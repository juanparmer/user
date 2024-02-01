# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from datetime import timedelta
from datetime import datetime
from odoo.exceptions import ValidationError
import calendar
import io
import xlwt
import base64
from odoo.exceptions import UserError
import uuid
import logging

_logger = logging.getLogger(__name__)
from datetime import date,datetime
from dateutil.relativedelta import relativedelta

PAYMENT_STATE_SELECTION = [
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('reversed', 'Reversed'),
        ('invoicing_legacy', 'Invoicing App Legacy'),
]

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def default_start_date(self):
        return datetime.now().date().replace(month=1, day=1)

    @api.model
    def default_end_date(self):
        return fields.Date.today()

    start_date = fields.Date("Start Date", default=default_start_date)
    end_date = fields.Date("End Date", default=default_end_date)
    sh_date_filter = fields.Selection([
        ('this_month','This Month'),
        ('last_month','Last Month'),
        ('this_quarter','This Quarter'),
        ('last_quarter','Last Quarter'),
        ('this_year','This Year'),
        ('last_year','Last Year'),
        ('custom','Custom'),
    ])
    

    sh_filter_customer_statement_ids = fields.One2many(
        "sh.res.partner.filter.statement",
        "partner_id",
        string="Customer Filtered Statements",
    )
    sh_customer_statement_ids = fields.One2many(
        "sh.customer.statement", "partner_id", string="Customer Statements"
    )
    sh_customer_zero_to_thiry = fields.Float("0-30")
    sh_customer_thirty_to_sixty = fields.Float("30-60")
    sh_customer_sixty_to_ninety = fields.Float("60-90")
    sh_customer_ninety_plus = fields.Float("90+")
    sh_customer_total = fields.Float("Total")
    sh_dont_send_customer_statement_auto = fields.Boolean("Don't send statement auto ?")
    sh_dont_send_due_customer_statement_auto = fields.Boolean(
        "Don't send Overdue statement auto ?"
    )
    sh_customer_due_statement_ids = fields.One2many(
        "sh.customer.due.statement", "partner_id", string="Customer Overdue Statements"
    )
    sh_customer_compute_boolean = fields.Boolean(
        "Boolean", compute="_compute_customer_statements"
    )
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )
    sh_cfs_statement_report_url = fields.Char(compute="_compute_cfs_report_url")
    sh_cust_statement_report_url = fields.Char(compute="_compute_cust_report_url")
    sh_cust_due_statement_report_url = fields.Char(
        compute="_compute_cust_due_report_url"
    )
    report_token = fields.Char("Access Token")
    portal_statement_url_wp = fields.Char(compute="_compute_statement_portal_url_wp")

    sh_customer_statement_config = fields.Many2many(
        "sh.customer.statement.config",
        string="Customer Statement Config",
        readonly=True,
    )
    payment_state = fields.Selection(PAYMENT_STATE_SELECTION, string="Payment Status")

    def _compute_statement_portal_url_wp(self):
        for rec in self:
            rec.portal_statement_url_wp = False
            if rec.company_id.sh_statement_url_in_message:
                base_url = (
                    self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                )
                ticket_url = ""
                if rec.customer_rank > 0:
                    ticket_url = base_url + "/my/customer_statements"
                rec.portal_statement_url_wp = ticket_url

    def _get_token(self):
        """Get the current record access token"""
        if self.report_token:
            return self.report_token
        else:
            report_token = str(uuid.uuid4())
            self.write({"report_token": report_token})
            return report_token

    def get_download_report_url(self):
        url = ""
        if self.id:
            self.ensure_one()
            url = "/download/cfs/" + "%s?access_token=%s" % (self.id, self._get_token())
        return url

    def get_cust_statement_download_report_url(self):
        url = ""
        if self.id:
            self.ensure_one()
            url = "/download/cs/" + "%s?access_token=%s" % (self.id, self._get_token())
        return url

    def get_cust_due_statement_download_report_url(self):
        url = ""
        if self.id:
            self.ensure_one()
            url = "/download/cds/" + "%s?access_token=%s" % (self.id, self._get_token())
        return url

    def _compute_cfs_report_url(self):
        for rec in self:
            rec.sh_cfs_statement_report_url = False
            if rec.company_id.sh_statement_pdf_in_message:
                base_url = (
                    self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                )
                if rec.customer_rank > 0:
                    rec.sh_cfs_statement_report_url = (
                        base_url + rec.get_download_report_url()
                    )

    def _compute_cust_report_url(self):
        for rec in self:
            rec.sh_cust_statement_report_url = False
            if rec.company_id.sh_statement_pdf_in_message:
                base_url = (
                    self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                )
                if rec.customer_rank > 0:
                    rec.sh_cust_statement_report_url = (
                        base_url + rec.get_cust_statement_download_report_url()
                    )

    def _compute_cust_due_report_url(self):
        for rec in self:
            rec.sh_cust_due_statement_report_url = False
            if rec.company_id.sh_statement_pdf_in_message:
                base_url = (
                    self.env["ir.config_parameter"].sudo().get_param("web.base.url")
                )
                if rec.customer_rank > 0:
                    rec.sh_cust_due_statement_report_url = (
                        base_url + rec.get_cust_due_statement_download_report_url()
                    )

    def _get_cfs_report_base_filename(self):
        self.ensure_one()
        return "%s %s" % ("Customer Statement Filter By Date", self.name)

    def _get_cs_report_base_filename(self):
        self.ensure_one()
        return "%s %s" % ("Customer Statement", self.name)

    def _get_cds_report_base_filename(self):
        self.ensure_one()
        return "%s %s" % ("Customer Due/Overdue Statement", self.name)

    def action_send_filter_customer_whatsapp(self):
        self.ensure_one()
        if not self.mobile:
            raise UserError(_("Partner Mobile Number Not Exist !"))
        template = self.env.ref(
            "sh_customer_statement.sh_send_customer_filter_whatsapp_email_template"
        )
        ctx = {
            "default_model": "res.partner",
            "default_res_id": self.ids[0],
            "default_use_template": bool(template.id),
            "default_template_id": template.id,
            "default_composition_mode": "comment",
            "force_email": True,
            "default_is_customer_statement": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }

    def action_send_customer_whatsapp(self):
        self.ensure_one()
        if not self.mobile:
            raise UserError(_("Partner Mobile Number Not Exist !"))
        template = self.env.ref(
            "sh_customer_statement.sh_send_customer_whatsapp_email_template"
        )
        ctx = {
            "default_model": "res.partner",
            "default_res_id": self.ids[0],
            "default_use_template": bool(template.id),
            "default_template_id": template.id,
            "default_composition_mode": "comment",
            "force_email": True,
            "default_is_customer_statement": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }

    def action_send_due_customer_whatsapp(self):
        self.ensure_one()
        if not self.mobile:
            raise UserError(_("Partner Mobile Number Not Exist !"))
        template = self.env.ref(
            "sh_customer_statement.sh_send_customer_due_whatsapp_email_template"
        )
        ctx = {
            "default_model": "res.partner",
            "default_res_id": self.ids[0],
            "default_use_template": bool(template.id),
            "default_template_id": template.id,
            "default_composition_mode": "comment",
            "force_email": True,
            "default_is_customer_statement": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": ctx,
        }

    def update_statement_config_manually_(self):
        view = self.env.ref(
            "sh_customer_statement.sh_update_customers_statement_config_wizard"
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Mass Update Config",
            "view_mode": "form",
            "views": [(view.id, "form")],
            "res_model": "sh.customer.config.mass.update",
            "view_id": view.id,
            "target": "new",
            "context": {"default_sh_selected_partner_ids": self.ids},
        }

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        if self.filtered(lambda c: c.end_date and c.start_date and c.start_date > c.end_date):
            raise ValidationError(_("start date must be less than end date."))

    def _compute_customer_statements(self):
        # =====================================================================
        # WRITE NEW METHOD FROM SCRACH 
        # =====================================================================
        for rec in self:
            rec.sh_customer_compute_boolean=True
            rec.sh_customer_statement_ids=[(6,0,[])]
            rec.sh_customer_due_statement_ids=[(6,0,[])]
            
            # ================================================================================
            # PREAPRE DATA FOR CUSTOMER STATEMENT WHICH PARTNER HAS CUSTOMER RANK MORE THAN 0
            # ================================================================================
            
            if rec.customer_rank > 0:
                
                # ------- GET DATA OF INVOICE AND CREDIT NOTE FOR CURRENT PARTNER ----------
                
                self._cr.execute(""" select id from account_move where partner_id=%s and move_type in ('out_invoice','out_refund') and state not in ('draft','cancel')  """,[rec.id,])
                c_moves_statements=self._cr.dictfetchall()
                c_moves_statements=self.env['account.move'].browse([r['id'] for r in c_moves_statements])
                
                # ------- CREATE CUSTOMER STATEMENT LINE FROM INVOICE ----------
                for move in c_moves_statements.filtered(lambda i:i.move_type=='out_invoice'):
                    statement_vals = {
                        "sh_account": rec.property_account_receivable_id.name,
                        "name": move.name,
                        "currency_id": move.currency_id.id,
                        "sh_customer_invoice_date": move.invoice_date,
                        "sh_customer_due_date": move.invoice_date_due,
                        "sh_customer_amount": move.amount_total,
                        "sh_customer_paid_amount": move.amount_total
                        - move.amount_residual,
                        "sh_customer_balance": move.amount_residual,
                        "partner_id":rec.id,
                    }
                    self.env['sh.customer.statement'].create(statement_vals)
                    
                # ------- CREATE CUSTOMER STATEMENT LINE FROM CREDIT NOTE AND MULTIPLE WITH -1 BECAUSE IT REVERSE OF INVOICE  ----------    
                for move in c_moves_statements.filtered(lambda i:i.move_type=='out_refund'):
                    statement_vals = {
                        "sh_account": rec.property_account_receivable_id.name,
                        "name": move.name,
                        "currency_id": move.currency_id.id,
                        "sh_customer_invoice_date": move.invoice_date,
                        "sh_customer_due_date": move.invoice_date_due,
                        "sh_customer_amount": move.amount_total*-1,
                        "sh_customer_paid_amount": (move.amount_total
                        - move.amount_residual)*-1,
                        "sh_customer_balance": (move.amount_residual)*-1,
                        "partner_id":rec.id,
                    }
                    self.env['sh.customer.statement'].create(statement_vals)
                
                # ================================================================================
                # GET PAYMENT OF CURRENT PARTNER WHICH IS NOT FULLY RECONCILE AND CUSTOMER 
                # RECEVING PAYMENT AND VENDOR SENDED PAYMENT
                # ================================================================================
                
                self._cr.execute(""" select id from account_payment where partner_id=%s and is_reconciled=False and partner_type='customer'  """,[rec.id,])
                customer_payment=self._cr.dictfetchall()
                customer_payment=self.env['account.payment'].sudo().browse([r['id'] for r in customer_payment])
                
                # ------- CREATE CUSTOMER STATEMENT LINE FROM CUSTOMER INBOUND (RECEVING) PAYMENT ----------
                for payment in customer_payment.filtered(lambda i:i.payment_type=='inbound' and i.state=='posted'):
                    domain = [
                        ('account_id.account_type', 'in',('asset_receivable', 'liability_payable')),
                        ('parent_state', '=', 'posted'),
                        ('payment_id', '=', payment.id),
                    ]
                    unpaid_move=self.env['account.move.line'].search(domain)
                    unpaid_amount=sum(unpaid_move.mapped('amount_residual_currency'))
                    statement_vals = {
                        "sh_account": rec.property_account_receivable_id.name,
                        "name": payment.name,
                        "currency_id": payment.currency_id.id,
                        "sh_customer_invoice_date": payment.date,
                        "sh_customer_amount": 0,
                        "sh_customer_paid_amount": abs(unpaid_amount) ,
                        "sh_customer_balance": unpaid_amount ,
                        "partner_id":rec.id,
                    }
                    self.env['sh.customer.statement'].create(statement_vals) 
                
                # ------- CREATE CUSTOMER STATEMENT LINE FROM VENDOR OUTBOUND (SENDING) PAYMENT ----------
                for payment in customer_payment.filtered(lambda i:i.payment_type=='outbound' and i.state=='posted'):
                    domain = [
                        ('account_id.account_type', 'in',('asset_receivable', 'liability_payable')),
                        ('parent_state', '=', 'posted'),
                        ('payment_id', '=', payment.id),
                    ]
                    unpaid_move=self.env['account.move.line'].search(domain)
                    unpaid_amount=sum(unpaid_move.mapped('amount_residual_currency'))
                    statement_vals = {
                        "sh_account": rec.property_account_receivable_id.name,
                        "name": payment.name,
                        "currency_id": payment.currency_id.id,
                        "sh_customer_invoice_date": payment.date,
                        "sh_customer_amount": 0,
                        "sh_customer_paid_amount": abs(unpaid_amount) ,
                        "sh_customer_balance": unpaid_amount ,
                        "partner_id":rec.id,
                    }
                    self.env['sh.customer.statement'].create(statement_vals)     
                
                #  ==================================================================
                #  CALCULATE AGING FROM INVOICE AND PAYMENT OF CUSTOMER 
                #  ==================================================================
                current_date=date.today()
                
                # --------- CALCULATE 0 TO 30 DAYS BALANCE AMOUNT -----------------
                
                self._cr.execute(""" select id,amount_residual from account_move where partner_id=%s and move_type ='out_invoice' and invoice_date<=%s and  invoice_date>%s  and state not in ('draft','cancel') """,[rec.id,current_date,current_date-timedelta(days=30)])
                invoice_due_amount_0_to_30=self._cr.dictfetchall()
                invoice_due_amount_0_to_30=sum([sub['amount_residual'] for sub in invoice_due_amount_0_to_30 ])
                self._cr.execute(""" select id,amount_residual from account_move where partner_id=%s and move_type ='out_refund' and invoice_date<=%s and  invoice_date>%s  and state not in ('draft','cancel') """,[rec.id,current_date,current_date-timedelta(days=30)])
                credit_note_due_amount_0_to_30=self._cr.dictfetchall()
                credit_note_due_amount_0_to_30=sum([sub['amount_residual'] for sub in credit_note_due_amount_0_to_30 ]) 
                payment_0_to_30=customer_payment.filtered(lambda i:i.state=='posted' and i.date<=current_date and i.date>current_date-timedelta(days=30))
                payment_due_amount_0_to_30=0
                if payment_0_to_30:
                    self._cr.execute(""" select id,amount_residual_currency from account_move_line where account_id in (select id from account_account where account_type in ('asset_receivable','liability_payable')) and parent_state='posted' and payment_id in %s   """,[tuple(payment_0_to_30.ids),])
                    payment_due_amount_0_to_30=self._cr.dictfetchall()
                    payment_due_amount_0_to_30=sum([sub['amount_residual_currency'] for sub in payment_due_amount_0_to_30 ])
                rec.sh_customer_zero_to_thiry=invoice_due_amount_0_to_30-credit_note_due_amount_0_to_30+payment_due_amount_0_to_30    
                   
                # --------- CALCULATE 30 TO 60 DAYS BALANCE AMOUNT -----------------
                
                self._cr.execute(""" select id,amount_residual from account_move where partner_id=%s and move_type ='out_invoice' and invoice_date<=%s and  invoice_date>%s  and state not in ('draft','cancel') """,[rec.id,current_date-timedelta(days=30),current_date-timedelta(days=60)])
                invoice_due_amount_30_to_60=self._cr.dictfetchall()
                invoice_due_amount_30_to_60=sum([sub['amount_residual'] for sub in invoice_due_amount_30_to_60 ])
                self._cr.execute(""" select id,amount_residual from account_move where partner_id=%s and move_type ='out_refund' and invoice_date<=%s and  invoice_date>%s  and state not in ('draft','cancel') """,[rec.id,current_date-timedelta(days=30),current_date-timedelta(days=60)])
                credit_note_due_amount_30_to_60=self._cr.dictfetchall()
                credit_note_due_amount_30_to_60=sum([sub['amount_residual'] for sub in credit_note_due_amount_30_to_60 ]) 
                payment_30_to_60=customer_payment.filtered(lambda i:i.state=='posted' and i.date<=current_date-timedelta(days=30) and i.date>current_date-timedelta(days=60))
                payment_due_amount_30_to_60=0
                if payment_30_to_60:
                    self._cr.execute(""" select id,amount_residual_currency from account_move_line where account_id in (select id from account_account where account_type in ('asset_receivable','liability_payable')) and parent_state='posted' and payment_id in %s   """,[tuple(payment_30_to_60.ids),])
                    payment_due_amount_30_to_60=self._cr.dictfetchall()
                    payment_due_amount_30_to_60=sum([sub['amount_residual_currency'] for sub in payment_due_amount_30_to_60 ])
                rec.sh_customer_thirty_to_sixty=invoice_due_amount_30_to_60-credit_note_due_amount_30_to_60+payment_due_amount_30_to_60 
                
                # --------- CALCULATE 60 TO 90 DAYS BALANCE AMOUNT -----------------
                
                self._cr.execute(""" select id,amount_residual from account_move where partner_id=%s and move_type ='out_invoice' and invoice_date<=%s and  invoice_date>%s  and state not in ('draft','cancel') """,[rec.id,current_date-timedelta(days=60),current_date-timedelta(days=90)])
                invoice_due_amount_60_to_90=self._cr.dictfetchall()
                invoice_due_amount_60_to_90=sum([sub['amount_residual'] for sub in invoice_due_amount_60_to_90 ])
                self._cr.execute(""" select id,amount_residual from account_move where partner_id=%s and move_type ='out_refund' and invoice_date<=%s and  invoice_date>%s  and state not in ('draft','cancel') """,[rec.id,current_date-timedelta(days=60),current_date-timedelta(days=90)])
                credit_note_due_amount_60_to_90=self._cr.dictfetchall()
                credit_note_due_amount_60_to_90=sum([sub['amount_residual'] for sub in credit_note_due_amount_60_to_90 ]) 
                payment_60_to_90=customer_payment.filtered(lambda i:i.state=='posted' and i.date<=current_date-timedelta(days=60) and i.date>current_date-timedelta(days=90))
                payment_due_amount_60_to_90=0
                if payment_60_to_90:
                    self._cr.execute(""" select id,amount_residual_currency from account_move_line where account_id in (select id from account_account where account_type in ('asset_receivable','liability_payable')) and parent_state='posted' and payment_id in %s   """,[tuple(payment_60_to_90.ids),])
                    payment_due_amount_60_to_90=self._cr.dictfetchall()
                    payment_due_amount_60_to_90=sum([sub['amount_residual_currency'] for sub in payment_due_amount_60_to_90 ])
                rec.sh_customer_sixty_to_ninety=invoice_due_amount_60_to_90-credit_note_due_amount_60_to_90+payment_due_amount_60_to_90 
                
                # --------- CALCULATE 30 TO 60 DAYS BALANCE AMOUNT -----------------
                
                self._cr.execute(""" select id,amount_residual from account_move where partner_id=%s and move_type ='out_invoice' and invoice_date<=%s  and state not in ('draft','cancel')  """,[rec.id,current_date-timedelta(days=90)])
                invoice_due_amount_90_plus=self._cr.dictfetchall()
                invoice_due_amount_90_plus=sum([sub['amount_residual'] for sub in invoice_due_amount_90_plus ])
                self._cr.execute(""" select id,amount_residual from account_move where partner_id=%s and move_type ='out_refund' and invoice_date<=%s  and state not in ('draft','cancel')  """,[rec.id,current_date-timedelta(days=90)])
                credit_note_due_amount_90_plus=self._cr.dictfetchall()
                credit_note_due_amount_90_plus=sum([sub['amount_residual'] for sub in credit_note_due_amount_90_plus ]) 
                payment_90_plus=customer_payment.filtered(lambda i:i.state=='posted' and i.date<=current_date-timedelta(days=90))
                payment_due_amount_90_plus=0
                if payment_90_plus:
                    self._cr.execute(""" select id,amount_residual_currency from account_move_line where account_id in (select id from account_account where account_type in ('asset_receivable','liability_payable')) and parent_state='posted' and payment_id in %s   """,[tuple(payment_90_plus.ids),])
                    payment_due_amount_90_plus=self._cr.dictfetchall()
                    payment_due_amount_90_plus=sum([sub['amount_residual_currency'] for sub in payment_due_amount_90_plus ])
                rec.sh_customer_ninety_plus=invoice_due_amount_90_plus-credit_note_due_amount_90_plus+payment_due_amount_90_plus  
                
                rec.sh_customer_total=rec.sh_customer_zero_to_thiry+rec.sh_customer_thirty_to_sixty+rec.sh_customer_sixty_to_ninety+rec.sh_customer_ninety_plus
                    
                #  ==================================================================
                #  OVERDUE STATEMENT LINE CREATE ACCORDING TO CONFIGURATION IN 
                #  ==================================================================      
                due_invoices=False
                if self.env.company.sh_display_due_statement =='due':
                    due_invoices=c_moves_statements.filtered(lambda x:x.amount_residual>0 and x.invoice_date_due >= current_date  )
                
                elif self.env.company.sh_display_due_statement =='overdue':
                    due_invoices=c_moves_statements.filtered(lambda x:x.amount_residual>0 and x.invoice_date_due < current_date  )
                elif self.env.company.sh_display_due_statement =='both':
                    due_invoices=c_moves_statements.filtered(lambda x:x.amount_residual>0 )
                if due_invoices:
                    for invoice in due_invoices.filtered(lambda i:i.move_type=='out_invoice'):
                        overdue_statement_vals = {
                            "sh_account": rec.property_account_receivable_id.name,
                            "currency_id": invoice.currency_id.id,
                            "name": invoice.name,
                            "sh_today": current_date,
                            "sh_due_customer_invoice_date": invoice.invoice_date,
                            "sh_due_customer_due_date": invoice.invoice_date_due,
                            "partner_id" :rec.id,
                            "sh_due_customer_amount": invoice.amount_total ,
                            "sh_due_customer_paid_amount":invoice.amount_total-invoice.amount_residual ,
                            "sh_due_customer_balance":invoice.amount_residual ,
                        }
                        self.env['sh.customer.due.statement'].create(overdue_statement_vals)
                        
                    # ------- CREATE CUSTOMER STATEMENT LINE FROM CREDIT NOTE AND MULTIPLE WITH -1 BECAUSE IT REVERSE OF INVOICE  ----------    
                    for invoice in due_invoices.filtered(lambda i:i.move_type=='out_refund'):
                        overdue_statement_vals = {
                            "sh_account": rec.property_account_receivable_id.name,
                            "currency_id": invoice.currency_id.id,
                            "name": invoice.name,
                            "sh_today": current_date,
                            "sh_due_customer_invoice_date": invoice.invoice_date,
                            "sh_due_customer_due_date": invoice.invoice_date_due,
                            "partner_id" :rec.id,
                            "sh_due_customer_amount": invoice.amount_total*-1 ,
                            "sh_due_customer_paid_amount":(invoice.amount_total-invoice.amount_residual)*-1 ,
                            "sh_due_customer_balance":invoice.amount_residual*-1 ,
                        }
                        self.env['sh.customer.due.statement'].create(overdue_statement_vals)
        
        
        # for rec in self:
        #     rec.sh_customer_compute_boolean = False
        #     if rec.customer_rank > 0:
        #         rec.sh_customer_statement_ids = False
        #         rec.sh_customer_due_statement_ids = False
        #         moves = (
        #             self.env["account.move"]
        #             .sudo()
        #             .search(
        #                 [
        #                     ("partner_id", "=", rec.id),
        #                     ("move_type", "in", ["out_invoice", "out_refund"]),
        #                     ("state", "not in", ["draft", "cancel"]),
        #                 ]
        #             )
        #         )

        #         statement_lines = []
        #         if moves:
        #             rec.sh_customer_statement_ids.unlink()

        #             for move in moves:
        #                 statement_vals = {
        #                     "sh_account": rec.property_account_receivable_id.name,
        #                     "name": move.name,
        #                     "currency_id": move.currency_id.id,
        #                     "sh_customer_invoice_date": move.invoice_date,
        #                     "sh_customer_due_date": move.invoice_date_due,
        #                 }
        #                 if move.move_type == "out_invoice":
        #                     statement_vals.update(
        #                         {
        #                             "sh_customer_amount": move.amount_total,
        #                             "sh_customer_paid_amount": move.amount_total
        #                             - move.amount_residual,
        #                             "sh_customer_balance": move.amount_total
        #                             - (move.amount_total - move.amount_residual),
        #                         }
        #                     )
        #                 elif move.move_type == "out_refund":
        #                     statement_vals.update(
        #                         {
        #                             "sh_customer_amount": move.amount_total
        #                             - move.amount_residual,
        #                             "sh_customer_paid_amount": move.amount_total,
        #                             "sh_customer_balance": (
        #                                 move.amount_total - move.amount_residual
        #                             )
        #                             - move.amount_total,
        #                         }
        #                     )
        #                 statement_lines.append((0, 0, statement_vals))
        #             rec.sh_customer_zero_to_thiry = 0.0
        #             rec.sh_customer_thirty_to_sixty = 0.0
        #             rec.sh_customer_sixty_to_ninety = 0.0
        #             rec.sh_customer_ninety_plus = 0.0
        #             today = fields.Date.today()
        #             date_before_30 = today - timedelta(days=30)
        #             date_before_60 = date_before_30 - timedelta(days=30)
        #             date_before_90 = date_before_60 - timedelta(days=30)
        #             moves_before_30_days = (
        #                 self.env["account.move"]
        #                 .sudo()
        #                 .search(
        #                     [
        #                         ("move_type", "in", ["out_invoice", "out_refund"]),
        #                         ("partner_id", "=", rec.id),
        #                         ("invoice_date", ">=", date_before_30),
        #                         ("invoice_date", "<=", fields.Date.today()),
        #                         ("state", "not in", ["draft", "cancel"]),
        #                     ]
        #                 )
        #             )

        #             payments_before_30_days = (
        #                 self.env["account.payment"]
        #                 .sudo()
        #                 .search(
        #                     [
        #                         ("partner_id", "=", rec.id),
        #                         ("state", "in", ["posted"]),
        #                         ("date", ">=", date_before_30),
        #                         ("date", "<=", fields.Date.today()),
        #                         ("partner_type", "in", ["customer"]),
        #                     ]
        #                 )
        #             )

        #             moves_before_60_days = (
        #                 self.env["account.move"]
        #                 .sudo()
        #                 .search(
        #                     [
        #                         ("move_type", "in", ["out_invoice", "out_refund"]),
        #                         ("partner_id", "=", rec.id),
        #                         ("invoice_date", ">=", date_before_60),
        #                         ("invoice_date", "<", date_before_30),
        #                         ("state", "not in", ["draft", "cancel"]),
        #                     ]
        #                 )
        #             )

        #             payments_before_60_days = (
        #                 self.env["account.payment"]
        #                 .sudo()
        #                 .search(
        #                     [
        #                         ("partner_id", "=", rec.id),
        #                         ("state", "in", ["posted"]),
        #                         ("date", ">=", date_before_60),
        #                         ("date", "<", date_before_30),
        #                         ("partner_type", "in", ["customer"]),
        #                     ]
        #                 )
        #             )

        #             moves_before_90_days = (
        #                 self.env["account.move"]
        #                 .sudo()
        #                 .search(
        #                     [
        #                         ("move_type", "in", ["out_invoice", "out_refund"]),
        #                         ("partner_id", "=", rec.id),
        #                         ("invoice_date", ">=", date_before_90),
        #                         ("invoice_date", "<", date_before_60),
        #                         ("state", "not in", ["draft", "cancel"]),
        #                     ]
        #                 )
        #             )

        #             payments_before_90_days = (
        #                 self.env["account.payment"]
        #                 .sudo()
        #                 .search(
        #                     [
        #                         ("partner_id", "=", rec.id),
        #                         ("state", "in", ["posted"]),
        #                         ("date", ">=", date_before_90),
        #                         ("date", "<", date_before_60),
        #                         ("partner_type", "in", ["customer"]),
        #                     ]
        #                 )
        #             )

        #             moves_90_plus = (
        #                 self.env["account.move"]
        #                 .sudo()
        #                 .search(
        #                     [
        #                         ("move_type", "in", ["out_invoice", "out_refund"]),
        #                         ("partner_id", "=", rec.id),
        #                         ("invoice_date", "<", date_before_90),
        #                         ("state", "not in", ["draft", "cancel"]),
        #                     ]
        #                 )
        #             )

        #             payments_90_plus = (
        #                 self.env["account.payment"]
        #                 .sudo()
        #                 .search(
        #                     [
        #                         ("partner_id", "=", rec.id),
        #                         ("state", "in", ["posted"]),
        #                         ("date", "<", date_before_90),
        #                         ("partner_type", "in", ["customer"]),
        #                     ]
        #                 )
        #             )

        #             if moves_before_30_days or payments_before_30_days:
        #                 total_paid = 0.0
        #                 total_amount = 0.0
        #                 total_balance = 0.0
        #                 for move_before_30 in moves_before_30_days:
        #                     if move_before_30.move_type == "out_invoice":
        #                         total_amount += move_before_30.amount_total
        #                         # total_paid += move_before_30.amount_total - move_before_30.amount_residual
        #                     elif move_before_30.move_type == "out_refund":
        #                         total_paid += move_before_30.amount_total
        #                         # total_paid += -(move_before_30.amount_total - move_before_30.amount_residual)

        #                 for payments_before_30_day in payments_before_30_days:
        #                     if payments_before_30_day.payment_type == "inbound":
        #                         total_paid = total_paid + payments_before_30_day.amount
        #                     else:
        #                         total_amount = (
        #                             total_amount + payments_before_30_day.amount
        #                         )

        #                 total_balance = total_amount - total_paid
        #                 rec.sh_customer_zero_to_thiry = total_balance
        #             if moves_before_60_days or payments_before_60_days:
        #                 total_paid = 0.0
        #                 total_amount = 0.0
        #                 total_balance = 0.0
        #                 for move_before_60 in moves_before_60_days:
        #                     if move_before_60.move_type == "out_invoice":
        #                         total_amount += move_before_60.amount_total
        #                         # total_paid += move_before_60.amount_total - move_before_60.amount_residual
        #                     elif move_before_60.move_type == "out_refund":
        #                         total_paid += move_before_60.amount_total
        #                         # total_paid += -(move_before_60.amount_total - move_before_60.amount_residual)

        #                 for payments_before_60_day in payments_before_60_days:
        #                     if payments_before_60_day.payment_type == "inbound":
        #                         total_paid = total_paid + payments_before_60_day.amount
        #                     else:
        #                         total_amount = (
        #                             total_amount + payments_before_60_day.amount
        #                         )

        #                 total_balance = total_amount - total_paid
        #                 total_balance = total_amount - total_paid
        #                 rec.sh_customer_thirty_to_sixty = total_balance
        #             if moves_before_90_days or payments_before_90_days:
        #                 total_paid = 0.0
        #                 total_amount = 0.0
        #                 total_balance = 0.0
        #                 for move_before_90 in moves_before_90_days:
        #                     if move_before_90.move_type == "out_invoice":
        #                         total_amount += move_before_90.amount_total
        #                         # total_paid += move_before_90.amount_total - move_before_90.amount_residual
        #                     elif move_before_90.move_type == "out_refund":
        #                         total_paid += move_before_90.amount_total
        #                         # total_paid += -(move_before_90.amount_total - move_before_90.amount_residual)

        #                 for payments_before_90_day in payments_before_90_days:
        #                     if payments_before_90_day.payment_type == "inbound":
        #                         total_paid = total_paid + payments_before_90_day.amount
        #                     else:
        #                         total_amount = (
        #                             total_amount + payments_before_90_day.amount
        #                         )

        #                 total_balance = total_amount - total_paid
        #                 rec.sh_customer_sixty_to_ninety = total_balance

        #             if moves_90_plus or payments_90_plus:
        #                 total_paid = 0.0
        #                 total_amount = 0.0
        #                 total_balance = 0.0
        #                 for move_90_plus in moves_90_plus:
        #                     if move_90_plus.move_type == "out_invoice":
        #                         total_amount += move_90_plus.amount_total
        #                         # total_paid += move_90_plus.amount_total - move_90_plus.amount_residual
        #                     elif move_90_plus.move_type == "out_refund":
        #                         total_paid += move_90_plus.amount_total
        #                         # total_paid += -(move_90_plus.amount_total - move_90_plus.amount_residual)

        #                 for payment_90_plus in payments_90_plus:
        #                     if payment_90_plus.payment_type == "inbound":
        #                         total_paid = total_paid + payment_90_plus.amount
        #                     else:
        #                         total_amount = total_amount + payment_90_plus.amount

        #                 total_balance = total_amount - total_paid
        #                 rec.sh_customer_ninety_plus = total_balance
        #             rec.sh_customer_total = (
        #                 rec.sh_customer_zero_to_thiry
        #                 + rec.sh_customer_thirty_to_sixty
        #                 + rec.sh_customer_sixty_to_ninety
        #                 + rec.sh_customer_ninety_plus
        #             )

        #         advanced_payments_inbound = (
        #             self.env["account.payment"]
        #             .sudo()
        #             .search(
        #                 [
        #                     ("partner_id", "=", rec.id),
        #                     ("state", "in", ["posted"]),
        #                     ("payment_type", "in", ["inbound"]),
        #                     ("partner_type", "in", ["customer"]),
        #                 ]
        #             )
        #         )
        #         if advanced_payments_inbound:
        #             for advance_payment in advanced_payments_inbound:
        #                 total_paid_amount = 0.0
        #                 if advance_payment.reconciled_invoice_ids:
        #                     advance_payment_amount = advance_payment.amount
        #                     for invoice in advance_payment.reconciled_invoice_ids:
        #                         total_paid_amount += (
        #                             invoice.amount_total - invoice.amount_residual
        #                         )
        #                     if total_paid_amount < advance_payment_amount:
        #                         statement_vals = {
        #                             "sh_account": advance_payment.destination_account_id.name,
        #                             "name": advance_payment.name,
        #                             "currency_id": advance_payment.currency_id.id,
        #                             "sh_customer_invoice_date": advance_payment.date,
        #                             "sh_customer_amount": 0.0,
        #                             "sh_customer_paid_amount": advance_payment.amount
        #                             - total_paid_amount,
        #                             "sh_customer_balance": -(
        #                                 advance_payment.amount - total_paid_amount
        #                             ),
        #                         }
        #                         statement_lines.append((0, 0, statement_vals))
        #                 else:
        #                     statement_vals = {
        #                         "sh_account": advance_payment.destination_account_id.name,
        #                         "name": advance_payment.name,
        #                         "currency_id": advance_payment.currency_id.id,
        #                         "sh_customer_invoice_date": advance_payment.date,
        #                         "sh_customer_amount": 0.0,
        #                         "sh_customer_paid_amount": advance_payment.amount,
        #                         "sh_customer_balance": -(advance_payment.amount),
        #                     }
        #                     statement_lines.append((0, 0, statement_vals))

        #         advanced_payments_outbound = (
        #             self.env["account.payment"]
        #             .sudo()
        #             .search(
        #                 [
        #                     ("partner_id", "=", rec.id),
        #                     ("state", "in", ["posted"]),
        #                     ("payment_type", "in", ["outbound"]),
        #                     ("partner_type", "in", ["customer"]),
        #                 ]
        #             )
        #         )
        #         if advanced_payments_outbound:
        #             for advance_payment in advanced_payments_outbound:
        #                 total_paid_amount = 0.0
        #                 if advance_payment.reconciled_invoice_ids:
        #                     advance_payment_amount = advance_payment.amount
        #                     for invoice in advance_payment.reconciled_invoice_ids:
        #                         total_paid_amount += (
        #                             invoice.amount_total - invoice.amount_residual
        #                         )
        #                     if total_paid_amount < advance_payment_amount:
        #                         statement_vals = {
        #                             "sh_account": advance_payment.destination_account_id.name,
        #                             "name": advance_payment.name,
        #                             "currency_id": advance_payment.currency_id.id,
        #                             "sh_customer_invoice_date": advance_payment.date,
        #                             "sh_customer_amount": advance_payment.amount
        #                             - total_paid_amount,
        #                             "sh_customer_paid_amount": 0.0,
        #                             "sh_customer_balance": advance_payment.amount
        #                             - total_paid_amount,
        #                         }
        #                         statement_lines.append((0, 0, statement_vals))
        #                 else:
        #                     statement_vals = {
        #                         "sh_account": advance_payment.destination_account_id.name,
        #                         "name": advance_payment.name,
        #                         "currency_id": advance_payment.currency_id.id,
        #                         "sh_customer_invoice_date": advance_payment.date,
        #                         "sh_customer_amount": advance_payment.amount,
        #                         "sh_customer_paid_amount": 0.0,
        #                         "sh_customer_balance": advance_payment.amount,
        #                     }
        #                     statement_lines.append((0, 0, statement_vals))

        #         rec.sh_customer_statement_ids = statement_lines

        #         overdue_moves = False
        #         if self.env.company.sh_display_due_statement == "due":
        #             overdue_moves = moves.filtered(
        #                 lambda x: x.invoice_date_due
        #                 and x.invoice_date_due >= fields.Date.today()
        #                 and x.amount_residual > 0.00
        #             )
        #         elif self.env.company.sh_display_due_statement == "overdue":
        #             overdue_moves = moves.filtered(
        #                 lambda x: x.invoice_date_due
        #                 and x.invoice_date_due < fields.Date.today()
        #                 and x.amount_residual > 0.00
        #             )
        #         elif self.env.company.sh_display_due_statement == "both":
        #             overdue_moves = moves.filtered(lambda x: x.amount_residual > 0.00)
        #         if overdue_moves:
        #             rec.sh_customer_due_statement_ids.unlink()
        #             overdue_statement_lines = []
        #             for overdue in overdue_moves:
        #                 overdue_statement_vals = {
        #                     "sh_account": rec.property_account_receivable_id.name,
        #                     "currency_id": overdue.currency_id.id,
        #                     "name": overdue.name,
        #                     "sh_today": fields.Date.today(),
        #                     "sh_due_customer_invoice_date": overdue.invoice_date,
        #                     "sh_due_customer_due_date": overdue.invoice_date_due,
        #                 }
        #                 if overdue.move_type == "out_invoice":
        #                     overdue_statement_vals.update(
        #                         {
        #                             "sh_due_customer_amount": overdue.amount_total,
        #                             "sh_due_customer_paid_amount": overdue.amount_total
        #                             - overdue.amount_residual,
        #                             "sh_due_customer_balance": overdue.amount_total
        #                             - (overdue.amount_total - overdue.amount_residual),
        #                         }
        #                     )
        #                 elif overdue.move_type == "out_refund":
        #                     overdue_statement_vals.update(
        #                         {
        #                             "sh_due_customer_amount": (
        #                                 overdue.amount_total - overdue.amount_residual
        #                             ),
        #                             "sh_due_customer_paid_amount": overdue.amount_total,
        #                             "sh_due_customer_balance": (
        #                                 overdue.amount_total - overdue.amount_residual
        #                             )
        #                             - overdue.amount_total,
        #                         }
        #                     )
        #                 overdue_statement_lines.append((0, 0, overdue_statement_vals))

        #             rec.sh_customer_due_statement_ids = overdue_statement_lines

    def send_customer_statement(self):
        for rec in self:
            if rec.customer_rank > 0 and rec.sh_customer_statement_ids:
                template = self.env.ref(
                    "sh_customer_statement.sh_customer_statement_mail_template"
                )
                if template:
                    mail = template.sudo().send_mail(rec.id, force_send=True)
                    mail_id = self.env["mail.mail"].sudo().browse(mail)
                    if mail_id:
                        self.env["sh.customer.mail.history"].sudo().create(
                            {
                                "name": "Customer Account Statement",
                                "sh_statement_type": "customer_statement",
                                "sh_current_date": fields.Datetime.now(),
                                "sh_partner_id": rec.id,
                                "sh_mail_id": mail_id.id,
                                "sh_mail_status": mail_id.state,
                            }
                        )

    def send_customer_overdue_statement(self):
        for rec in self:
            if rec.customer_rank > 0 and rec.sh_customer_due_statement_ids:
                template = self.env.ref(
                    "sh_customer_statement.sh_customer_due_statement_mail_template"
                )
                if template:
                    mail = template.sudo().send_mail(rec.id, force_send=True)
                    mail_id = self.env["mail.mail"].sudo().browse(mail)
                    if mail_id:
                        self.env["sh.customer.mail.history"].sudo().create(
                            {
                                "name": "Customer Account Overdue Statement",
                                "sh_statement_type": "customer_overdue_statement",
                                "sh_current_date": fields.Datetime.now(),
                                "sh_partner_id": rec.id,
                                "sh_mail_id": mail_id.id,
                                "sh_mail_status": mail_id.state,
                            }
                        )

    def action_print_customer_statement(self):
        return self.env.ref(
            "sh_customer_statement.action_report_sh_customer_statement"
        ).report_action(self)

    def action_send_customer_statement(self):
        self.ensure_one()
        template = self.env.ref(
            "sh_customer_statement.sh_customer_statement_mail_template"
        )
        if template:
            mail = template.sudo().send_mail(self.id, force_send=True)
            mail_id = self.env["mail.mail"].sudo().browse(mail)
            if mail_id:
                self.env["sh.customer.mail.history"].sudo().create(
                    {
                        "name": "Customer Account Statement",
                        "sh_statement_type": "customer_statement",
                        "sh_current_date": fields.Datetime.now(),
                        "sh_partner_id": self.id,
                        "sh_mail_id": mail_id.id,
                        "sh_mail_status": mail_id.state,
                    }
                )

    def action_print_customer_due_statement(self):
        return self.env.ref(
            "sh_customer_statement.action_report_sh_customer_due_statement"
        ).report_action(self)

    def action_send_customer_due_statement(self):
        self.ensure_one()
        template = self.env.ref(
            "sh_customer_statement.sh_customer_due_statement_mail_template"
        )
        if template:
            mail = template.sudo().send_mail(self.id, force_send=True)
            mail_id = self.env["mail.mail"].sudo().browse(mail)
            if mail_id:
                self.env["sh.customer.mail.history"].sudo().create(
                    {
                        "name": "Customer Account Overdue Statement",
                        "sh_statement_type": "customer_overdue_statement",
                        "sh_current_date": fields.Datetime.now(),
                        "sh_partner_id": self.id,
                        "sh_mail_id": mail_id.id,
                        "sh_mail_status": mail_id.state,
                    }
                )

    def action_get_customer_statement(self):
        self.ensure_one()
        today = date.today()
        currQuarter = int((today.month - 1) / 3 + 1)
        if self.sh_date_filter!='custom':
            self.start_date=False
            self.end_date=False
        if self.sh_date_filter == 'this_month':
            self.start_date = date(today.year, today.month, 1)
            self.end_date  = date(today.year, today.month, calendar.mdays[today.month])

        if self.sh_date_filter == 'this_year':
            self.start_date = date(today.year, 1, 1)
            self.end_date = date(today.year, 12, 31)

        if self.sh_date_filter == 'last_month': 
            self.start_date = date(today.year, (today.month-1), 1)
            self.end_date = date(
                today.year, (today.month - 1), calendar.mdays[(today.month-1)])

        if self.sh_date_filter == 'last_year':
            self.start_date = date((today.year-1), 1, 1)
            self.end_date = date((today.year-1), 12, 31)

        if self.sh_date_filter == 'this_quarter':
            self.start_date = datetime(today.year, 3 * currQuarter - 2, 1)
            self.end_date = datetime(today.year, 3 * currQuarter + 1, 1) + timedelta(days=-1)
        
        if self.sh_date_filter == 'last_quarter':

            current_quar_start = datetime(today.year, 3 * currQuarter - 2, 1)

            self.start_date = datetime(today.year, current_quar_start.month, 1) + relativedelta(months=-3)
            self.end_date = current_quar_start + timedelta(days=-1)
            

        if self.customer_rank > 0 and self.start_date and self.end_date:

            self.sh_filter_customer_statement_ids.sudo().unlink()
            statement_lines = []

            account_id = self.property_account_receivable_id.id
            company_ids=[]
            if self.env.context and self.env.context.get('allowed_company_ids'):
                company_ids= self.env.context.get('allowed_company_ids')
            
            move_lines = self.env["account.move.line"].search(
                [
                    ("partner_id", "=", self.id),
                    ("date", "<", self.start_date),
                    ("account_id", "=", account_id),
                    ("parent_state", "=", "posted"),
                    ("company_id","in",company_ids)
                ]
            )

            balance = sum(move_lines.mapped("debit")) - sum(move_lines.mapped("credit"))

            statement_lines.append(
                (
                    0,
                    0,
                    {
                        "name": "Opening Balance",
                        "currency_id": move_lines[0].currency_id.id
                        if move_lines
                        else self.currency_id.id,
                        "sh_filter_balance": balance,
                    },
                )
            )
            if self.payment_state:
                moves = (
                    self.env["account.move"]
                    .sudo()
                    .search(
                        [
                            ("partner_id", "=", self.id),
                            ("move_type", "in", ["out_invoice", "out_refund"]),
                            ("invoice_date", ">=", self.start_date),
                            ("invoice_date", "<=", self.end_date),
                            ("state", "not in", ["draft", "cancel"]),
                            ('payment_state','=',self.payment_state),
                            ("company_id","in",company_ids)
                        ]
                    )
                )
            else:
                moves = (
                    self.env["account.move"]
                    .sudo()
                    .search(
                        [
                            ("partner_id", "=", self.id),
                            ("move_type", "in", ["out_invoice", "out_refund"]),
                            ("invoice_date", ">=", self.start_date),
                            ("invoice_date", "<=", self.end_date),
                            ("state", "not in", ["draft", "cancel"]),
                            ("company_id","in",company_ids)
                        ]
                    )
                )
            if moves:

                for move in moves:
                    statement_vals = {
                        "sh_account": self.property_account_receivable_id.name,
                        "name": move.name,
                        "currency_id": move.currency_id.id,
                        "sh_filter_invoice_date": move.invoice_date,
                        "sh_filter_due_date": move.invoice_date_due,
                    }
                    if move.move_type == "out_invoice":
                        statement_vals.update(
                            {
                                "sh_filter_amount": move.amount_total,
                                "sh_filter_paid_amount": move.amount_total
                                - move.amount_residual,
                                "sh_filter_balance": move.amount_total
                                - (move.amount_total - move.amount_residual),
                            }
                        )
                    elif move.move_type == "out_refund":
                        statement_vals.update(
                            {
                                "sh_filter_amount": move.amount_total*-1,
                                "sh_filter_paid_amount": (move.amount_total- move.amount_residual)*-1,
                                "sh_filter_balance": move.amount_residual*-1,
                            }
                        )
                    statement_lines.append((0, 0, statement_vals))

            advanced_payments_inbound = (
                self.env["account.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", self.id),
                        ("date", ">=", self.start_date),
                        ("date", "<=", self.end_date),
                        ("state", "in", ["posted"]),
                        ("payment_type", "in", ["inbound"]),
                        ("partner_type", "in", ["customer"]),
                        ("company_id","in",company_ids)
                    ]
                )
            )
            if advanced_payments_inbound:
                for advance_payment in advanced_payments_inbound:
                    total_paid_amount = 0.0                   
                    
                    domain = [
                        ('account_id.account_type', 'in',('asset_receivable', 'liability_payable')),
                        ('parent_state', '=', 'posted'),
                        ('payment_id', '=', advance_payment.id),
                        ("company_id","in",company_ids)
                    ]
                    unpaid_move=self.env['account.move.line'].search(domain)
                    if unpaid_move:
                        unpaid_amount=sum(unpaid_move.mapped('amount_residual_currency'))
                        advance_payment_amount = advance_payment.amount
                        total_paid_amount = advance_payment.amount-abs(unpaid_amount)
                        # if advance_payment.reconciled_invoice_ids:
                        #     for invoice in advance_payment.reconciled_invoice_ids:

                        #         if (
                        #             invoice.invoice_date >= self.start_date
                        #             and invoice.invoice_date <= self.end_date
                        #         ):


                        if total_paid_amount < advance_payment_amount:
                            statement_vals = {
                                "sh_account": advance_payment.destination_account_id.name,
                                "name": advance_payment.name,
                                "currency_id": advance_payment.currency_id.id,
                                "sh_filter_invoice_date": advance_payment.date,
                                "sh_filter_amount": 0.0,
                                "sh_filter_paid_amount": unpaid_amount,
                                "sh_filter_balance": unpaid_amount,
                            }
                            statement_lines.append((0, 0, statement_vals))
                    else:
                        statement_vals = {
                            "sh_account": advance_payment.destination_account_id.name,
                            "name": advance_payment.name,
                            "currency_id": advance_payment.currency_id.id,
                            "sh_filter_invoice_date": advance_payment.date,
                            "sh_filter_amount": 0.0,
                            "sh_filter_paid_amount": advance_payment.amount,
                            "sh_filter_balance": -(advance_payment.amount),
                        }
                        statement_lines.append((0, 0, statement_vals))

            advanced_payments_outbound = (
                self.env["account.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", self.id),
                        ("date", ">=", self.start_date),
                        ("date", "<=", self.end_date),
                        ("state", "in", ["posted"]),
                        ("payment_type", "in", ["outbound"]),
                        ("partner_type", "in", ["customer"]),
                        ("company_id","in",company_ids)
                    ]
                )
            )
            if advanced_payments_outbound:
                for advance_payment in advanced_payments_outbound:
                    total_paid_amount = 0.0
                    domain = [
                        ('account_id.account_type', 'in',('asset_receivable', 'liability_payable')),
                        ('parent_state', '=', 'posted'),
                        ('payment_id', '=', advance_payment.id),
                        ("company_id","in",company_ids)
                    ]
                    unpaid_move=self.env['account.move.line'].search(domain)
                    if unpaid_move:
                        unpaid_amount=sum(unpaid_move.mapped('amount_residual_currency'))
                        advance_payment_amount = advance_payment.amount
                    
                    
                    # if advance_payment.reconciled_invoice_ids:
                    #     for invoice in advance_payment.reconciled_invoice_ids:

                    #         if (
                    #             invoice.invoice_date >= self.start_date
                    #             and invoice.invoice_date <= self.end_date
                    #         ):

                    #             total_paid_amount += (
                    #                 invoice.amount_total - invoice.amount_residual
                    #             )
                        total_paid_amount=advance_payment_amount-unpaid_amount
                        if total_paid_amount < advance_payment_amount:
                            statement_vals = {
                                "sh_account": advance_payment.destination_account_id.name,
                                "name": advance_payment.name,
                                "currency_id": advance_payment.currency_id.id,
                                "sh_filter_invoice_date": advance_payment.date,
                                "sh_filter_amount": 0,
                                "sh_filter_paid_amount":unpaid_amount,
                                "sh_filter_balance": unpaid_amount,
                            }
                            statement_lines.append((0, 0, statement_vals))
                    else:
                        statement_vals = {
                            "sh_account": advance_payment.destination_account_id.name,
                            "name": advance_payment.name,
                            "currency_id": advance_payment.currency_id.id,
                            "sh_filter_invoice_date": advance_payment.date,
                            "sh_filter_amount": 0,
                            "sh_filter_paid_amount": unpaid_amount,
                            "sh_filter_balance": unpaid_amount,
                        }
                        statement_lines.append((0, 0, statement_vals))

            self.sh_filter_customer_statement_ids = statement_lines



    def action_print_filter_customer_statement(self):
        return self.env.ref(
            "sh_customer_statement.action_report_sh_customer_filtered_statement"
        ).report_action(self)

    def action_send_filter_customer_statement(self):
        self.ensure_one()
        template = self.env.ref(
            "sh_customer_statement.sh_customer_filter_statement_mail_template"
        )
        if template:
            mail = template.sudo().send_mail(self.id, force_send=True)
            mail_id = self.env["mail.mail"].sudo().browse(mail)
            if mail_id:
                self.env["sh.customer.mail.history"].sudo().create(
                    {
                        "name": "Customer Account Statement by Date",
                        "sh_statement_type": "customer_statement_filter",
                        "sh_current_date": fields.Datetime.now(),
                        "sh_partner_id": self.id,
                        "sh_mail_id": mail_id.id,
                        "sh_mail_status": mail_id.state,
                    }
                )

    def action_view_customer_history(self):
        self.ensure_one()
        return {
            "name": "Mail Log History",
            "type": "ir.actions.act_window",
            "res_model": "sh.customer.mail.history",
            "view_mode": "tree,form",
            "domain": [("sh_partner_id", "=", self.id)],
            "target": "current",
        }

    def action_print_filter_customer_statement_xls(self):
        workbook = xlwt.Workbook()
        heading_format = xlwt.easyxf(
            "font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        normal = xlwt.easyxf("font:bold True;align: horiz center;align: vert center")
        cyan_text = xlwt.easyxf(
            "font:bold True,color aqua;align: horiz center;align: vert center"
        )
        green_text = xlwt.easyxf(
            "font:bold True,color green;align: horiz center;align: vert center"
        )
        red_text = xlwt.easyxf(
            "font:bold True,color red;align: horiz center;align: vert center"
        )
        bold_center = xlwt.easyxf(
            "font:height 225,bold True;pattern: pattern solid,fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        date = xlwt.easyxf(
            "font:height 225,bold True;pattern: pattern solid,fore_colour gray25;align: vert center;align: horiz right;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        totals = xlwt.easyxf(
            "font:height 225,bold True;pattern: pattern solid,fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        worksheet = workbook.add_sheet(
            "Customer Statement Filter By Date", cell_overwrite_ok=True
        )

        worksheet.row(1).height = 380
        worksheet.row(2).height = 320
        worksheet.row(8).height = 400
        worksheet.col(2).width = 4800
        worksheet.col(3).width = 4800
        worksheet.col(4).width = 5500
        worksheet.col(5).width = 5500
        worksheet.col(6).width = 5500
        worksheet.col(0).width = 5500
        worksheet.col(1).width = 6000
        worksheet.write(1, 0, "Date From", date)
        if self.start_date:
            worksheet.write(1, 1, str(self.start_date), normal)
        worksheet.write(1, 2, "Date To", date)
        if self.end_date:
            worksheet.write(1, 3, str(self.end_date), normal)
        worksheet.write_merge(4, 5, 0, 6, self.name, heading_format)
        worksheet.write(8, 0, "Number", bold_center)
        worksheet.write(8, 1, "Account", bold_center)
        worksheet.write(8, 2, "Date", bold_center)
        worksheet.write(8, 3, "Due Date", bold_center)
        worksheet.write(8, 4, "Total Amount", bold_center)
        worksheet.write(8, 5, "Paid Amount", bold_center)
        worksheet.write(8, 6, "Balance", bold_center)

        total_amount = 0
        total_paid_amount = 0
        total_balance = 0
        k = 9

        if self.sh_filter_customer_statement_ids:
            for i in self.sh_filter_customer_statement_ids:
                for j in i:
                    worksheet.row(k).height = 350
                    if j.sh_filter_amount == j.sh_filter_balance:
                        if j.name == "Opening Balance":
                            worksheet.write(k, 0, j.name, green_text)
                            worksheet.write(k, 1, j.sh_account, green_text)
                            worksheet.write(
                                k, 2, str(j.sh_filter_invoice_date), green_text
                            )
                            if j.sh_filter_due_date:
                                worksheet.write(
                                    k, 3, str(j.sh_filter_due_date), green_text
                                )
                            else:
                                worksheet.write(k, 3, "", green_text)
                            worksheet.write(
                                k,
                                4,
                                str(i.currency_id.symbol)
                                + str("{:.2f}".format(j.sh_filter_amount)),
                                green_text,
                            )
                            worksheet.write(
                                k,
                                5,
                                str(i.currency_id.symbol)
                                + str("{:.2f}".format(j.sh_filter_paid_amount)),
                                green_text,
                            )
                            worksheet.write(
                                k,
                                6,
                                str(i.currency_id.symbol)
                                + str("{:.2f}".format(j.sh_filter_balance)),
                                green_text,
                            )
                        else:
                            worksheet.write(k, 0, j.name, cyan_text)
                            worksheet.write(k, 1, j.sh_account, cyan_text)
                            worksheet.write(
                                k, 2, str(j.sh_filter_invoice_date), cyan_text
                            )
                            if j.sh_filter_due_date:
                                worksheet.write(
                                    k, 3, str(j.sh_filter_due_date), cyan_text
                                )
                            else:
                                worksheet.write(k, 3, "", cyan_text)
                            worksheet.write(
                                k,
                                4,
                                str(i.currency_id.symbol)
                                + str("{:.2f}".format(j.sh_filter_amount)),
                                cyan_text,
                            )
                            worksheet.write(
                                k,
                                5,
                                str(i.currency_id.symbol)
                                + str("{:.2f}".format(j.sh_filter_paid_amount)),
                                cyan_text,
                            )
                            worksheet.write(
                                k,
                                6,
                                str(i.currency_id.symbol)
                                + str("{:.2f}".format(j.sh_filter_balance)),
                                cyan_text,
                            )
                    elif j.sh_filter_balance == 0:
                        worksheet.write(k, 0, j.name, green_text)
                        worksheet.write(k, 1, j.sh_account, green_text)
                        worksheet.write(k, 2, str(j.sh_filter_invoice_date), green_text)
                        if j.sh_filter_due_date:
                            worksheet.write(k, 3, str(j.sh_filter_due_date), green_text)
                        else:
                            worksheet.write(k, 3, "", green_text)
                        worksheet.write(
                            k,
                            4,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_filter_amount)),
                            green_text,
                        )
                        worksheet.write(
                            k,
                            5,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_filter_paid_amount)),
                            green_text,
                        )
                        worksheet.write(
                            k,
                            6,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_filter_balance)),
                            green_text,
                        )
                    else:
                        worksheet.write(k, 0, j.name, red_text)
                        worksheet.write(k, 1, j.sh_account, red_text)
                        worksheet.write(k, 2, str(j.sh_filter_invoice_date), red_text)
                        if j.sh_filter_due_date:
                            worksheet.write(k, 3, str(j.sh_filter_due_date), red_text)
                        else:
                            worksheet.write(k, 3, "", red_text)
                        worksheet.write(
                            k,
                            4,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_filter_amount)),
                            red_text,
                        )
                        worksheet.write(
                            k,
                            5,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_filter_paid_amount)),
                            red_text,
                        )
                        worksheet.write(
                            k,
                            6,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_filter_balance)),
                            red_text,
                        )
                    k = k + 1
                total_amount = total_amount + j.sh_filter_amount
                total_paid_amount = total_paid_amount + j.sh_filter_paid_amount
                total_balance = total_balance + j.sh_filter_balance
        if self.sh_filter_customer_statement_ids:
            worksheet.write(k, 4, str("{:.2f}".format(total_amount)), totals)
            worksheet.row(k).height = 350
            worksheet.write(k, 5, str("{:.2f}".format(total_paid_amount)), totals)
            worksheet.write(k, 6, str("{:.2f}".format(total_balance)), totals)

        fp = io.BytesIO()
        workbook.save(fp)
        data = base64.encodebytes(fp.getvalue())
        IrAttachment = self.env["ir.attachment"]
        attachment_vals = {
            "name": "Customer Statement Filter By Date.xls",
            "res_model": "ir.ui.view",
            "type": "binary",
            "datas": data,
            "public": True,
        }
        fp.close()

        attachment = IrAttachment.search(
            [
                ("name", "=", "Customer Statement Filter By Date"),
                ("type", "=", "binary"),
                ("res_model", "=", "ir.ui.view"),
            ],
            limit=1,
        )
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = IrAttachment.create(attachment_vals)
        # TODO: make user error here
        if not attachment:
            raise UserError("There is no attachments...")

        url = "/web/content/" + str(attachment.id) + "?download=true"
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "current",
        }

    def action_print_customer_statement_xls(self):
        workbook = xlwt.Workbook()
        heading_format = xlwt.easyxf(
            "font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        normal = xlwt.easyxf("font:bold True;align: horiz center;align: vert center")
        cyan_text = xlwt.easyxf(
            "font:bold True,color aqua;align: horiz center;align: vert center"
        )
        green_text = xlwt.easyxf(
            "font:bold True,color green;align: horiz center;align: vert center"
        )
        red_text = xlwt.easyxf(
            "font:bold True,color red;align: horiz center;align: vert center"
        )
        bold_center = xlwt.easyxf(
            "font:height 225,bold True;pattern: pattern solid,fore_colour gray25;align: horiz center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        totals = xlwt.easyxf(
            "font:height 225,bold True;pattern: pattern solid,fore_colour gray25;align: horiz center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        worksheet = workbook.add_sheet("Customer Statement", cell_overwrite_ok=True)

        worksheet.row(5).height = 400
        worksheet.row(12).height = 400
        worksheet.row(13).height = 400
        worksheet.row(10).height = 350
        worksheet.row(11).height = 350
        worksheet.col(2).width = 4800
        worksheet.col(3).width = 4800
        worksheet.col(4).width = 5500
        worksheet.col(5).width = 5500
        worksheet.col(6).width = 5500
        worksheet.col(0).width = 5500
        worksheet.col(1).width = 6000
        worksheet.write_merge(2, 3, 0, 6, self.name, heading_format)
        worksheet.write(5, 0, "Number", bold_center)
        worksheet.write(5, 1, "Account", bold_center)
        worksheet.write(5, 2, "Date", bold_center)
        worksheet.write(5, 3, "Due Date", bold_center)
        worksheet.write(5, 4, "Total Amount", bold_center)
        worksheet.write(5, 5, "Paid Amount", bold_center)
        worksheet.write(5, 6, "Balance", bold_center)

        total_amount = 0
        total_paid_amount = 0
        total_balance = 0
        k = 6

        if self.sh_customer_statement_ids:
            for i in self.sh_customer_statement_ids:
                for j in i:
                    worksheet.row(k).height = 350
                    if j.sh_customer_amount == j.sh_customer_balance:
                        worksheet.write(k, 0, j.name, cyan_text)
                        worksheet.write(k, 1, j.sh_account, cyan_text)
                        worksheet.write(
                            k, 2, str(j.sh_customer_invoice_date), cyan_text
                        )
                        if j.sh_customer_due_date:
                            worksheet.write(
                                k, 3, str(j.sh_customer_due_date), cyan_text
                            )
                        else:
                            worksheet.write(k, 3, "", cyan_text)
                        worksheet.write(
                            k,
                            4,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_amount)),
                            cyan_text,
                        )
                        worksheet.write(
                            k,
                            5,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_paid_amount)),
                            cyan_text,
                        )
                        worksheet.write(
                            k,
                            6,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_balance)),
                            cyan_text,
                        )
                    elif j.sh_customer_balance == 0:
                        worksheet.write(k, 0, j.name, green_text)
                        worksheet.write(k, 1, j.sh_account, green_text)
                        worksheet.write(
                            k, 2, str(j.sh_customer_invoice_date), green_text
                        )
                        if j.sh_customer_due_date:
                            worksheet.write(
                                k, 3, str(j.sh_customer_due_date), green_text
                            )
                        else:
                            worksheet.write(k, 3, "", green_text)
                        worksheet.write(
                            k,
                            4,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_amount)),
                            green_text,
                        )
                        worksheet.write(
                            k,
                            5,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_paid_amount)),
                            green_text,
                        )
                        worksheet.write(
                            k,
                            6,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_balance)),
                            green_text,
                        )
                    else:
                        worksheet.write(k, 0, j.name, red_text)
                        worksheet.write(k, 1, j.sh_account, red_text)
                        worksheet.write(k, 2, str(j.sh_customer_invoice_date), red_text)
                        if j.sh_customer_due_date:
                            worksheet.write(k, 3, str(j.sh_customer_due_date), red_text)
                        else:
                            worksheet.write(k, 3, "", red_text)
                        worksheet.write(
                            k,
                            4,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_amount)),
                            red_text,
                        )
                        worksheet.write(
                            k,
                            5,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_paid_amount)),
                            red_text,
                        )
                        worksheet.write(
                            k,
                            6,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_customer_balance)),
                            red_text,
                        )
                    k = k + 1
                total_amount = total_amount + float(
                    "{:.2f}".format(j.sh_customer_amount)
                )
                total_paid_amount = total_paid_amount + float(
                    "{:.2f}".format(j.sh_customer_paid_amount)
                )
                total_balance = total_balance + j.sh_customer_balance

        if self.sh_customer_statement_ids:
            worksheet.write(k, 4, str("{:.2f}".format(total_amount)), totals)
            worksheet.row(k).height = 350
            worksheet.write(k, 5, str("{:.2f}".format(total_paid_amount)), totals)
            worksheet.write(k, 6, str("{:.2f}".format(total_balance)), totals)
        worksheet.write(k + 3, 0, "Gap Between Days", bold_center)
        worksheet.write(k + 3, 1, "0-30(Days)", bold_center)
        worksheet.write(k + 3, 2, "30-60(Days)", bold_center)
        worksheet.write(k + 3, 3, "60-90(Days)", bold_center)
        worksheet.write(k + 3, 4, "90+(Days)", bold_center)
        worksheet.write(k + 3, 5, "Total", bold_center)
        worksheet.write(k + 4, 0, "Balance Amount", bold_center)
        if self.sh_customer_statement_ids:
            worksheet.write(
                k + 4, 1, str("{:.2f}".format(self.sh_customer_zero_to_thiry)), normal
            )
            worksheet.write(
                k + 4, 2, str("{:.2f}".format(self.sh_customer_thirty_to_sixty)), normal
            )
            worksheet.write(
                k + 4, 3, str("{:.2f}".format(self.sh_customer_sixty_to_ninety)), normal
            )
            worksheet.write(
                k + 4, 4, str("{:.2f}".format(self.sh_customer_ninety_plus)), normal
            )
            worksheet.write(
                k + 4, 5, str("{:.2f}".format(self.sh_customer_total)), normal
            )

        fp = io.BytesIO()
        workbook.save(fp)
        data = base64.encodebytes(fp.getvalue())
        IrAttachment = self.env["ir.attachment"]
        attachment_vals = {
            "name": "Customer Statement.xls",
            "res_model": "ir.ui.view",
            "type": "binary",
            "datas": data,
            "public": True,
        }
        fp.close()

        attachment = IrAttachment.search(
            [
                ("name", "=", "Customer Statement"),
                ("type", "=", "binary"),
                ("res_model", "=", "ir.ui.view"),
            ],
            limit=1,
        )
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = IrAttachment.create(attachment_vals)
        # TODO: make user error here
        if not attachment:
            raise UserError("There is no attachments...")

        url = "/web/content/" + str(attachment.id) + "?download=true"
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "current",
        }

    def action_print_customer_due_statement_xls(self):
        workbook = xlwt.Workbook()
        heading_format = xlwt.easyxf(
            "font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        red_text = xlwt.easyxf(
            "font:bold True,color red;align: horiz center;align: vert center"
        )
        center_text = xlwt.easyxf("align: horiz center;align: vert center")
        bold_center = xlwt.easyxf(
            "font:height 225,bold True;pattern: pattern solid,fore_colour gray25;align: horiz center;align: vert center;borders: left thin, right thin, bottom thin,top thin,top_color gray40,bottom_color gray40,left_color gray40,right_color gray40"
        )
        date = xlwt.easyxf(
            "font:height 225,bold True;pattern: pattern solid,fore_colour gray25;align: horiz center;borders: left thin, right thin, bottom thin;align: vert center;align: horiz left"
        )
        worksheet = workbook.add_sheet(
            "Customer Overdue Statement", cell_overwrite_ok=True
        )

        now = datetime.now()
        today_date = now.strftime("%d/%m/%Y %H:%M:%S")

        worksheet.write(1, 0, str(str("Date") + str(": ") + str(today_date)), date)
        worksheet.row(1).height = 350
        worksheet.row(6).height = 350
        worksheet.col(0).width = 8000
        worksheet.col(1).width = 6000
        worksheet.col(2).width = 4800
        worksheet.col(3).width = 4800
        worksheet.col(4).width = 5500
        worksheet.col(5).width = 5500
        worksheet.col(6).width = 5500
        worksheet.row(11).height = 350

        worksheet.write_merge(3, 4, 0, 6, self.name, heading_format)
        worksheet.write(6, 0, "Number", bold_center)
        worksheet.write(6, 1, "Account", bold_center)
        worksheet.write(6, 2, "Date", bold_center)
        worksheet.write(6, 3, "Due Date", bold_center)
        worksheet.write(6, 4, "Total Amount", bold_center)
        worksheet.write(6, 5, "Paid Amount", bold_center)
        worksheet.write(6, 6, "Balance", bold_center)

        total_amount = 0
        total_paid_amount = 0
        total_balance = 0
        k = 7

        if self.sh_customer_due_statement_ids:
            for i in self.sh_customer_due_statement_ids:
                worksheet.row(k).height = 350
                for j in i:
                    if (
                        j.sh_due_customer_due_date
                        and j.sh_today
                        and j.sh_due_customer_due_date < j.sh_today
                    ):
                        worksheet.write(k, 0, j.name, red_text)
                        worksheet.write(k, 1, j.sh_account, red_text)
                        worksheet.write(
                            k, 2, str(j.sh_due_customer_invoice_date), red_text
                        )
                        if j.sh_due_customer_due_date:
                            worksheet.write(
                                k, 3, str(j.sh_due_customer_due_date), red_text
                            )
                        else:
                            worksheet.write(k, 3, "", red_text)
                        worksheet.write(
                            k,
                            4,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_due_customer_amount)),
                            red_text,
                        )
                        worksheet.write(
                            k,
                            5,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_due_customer_paid_amount)),
                            red_text,
                        )
                        worksheet.write(
                            k,
                            6,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_due_customer_balance)),
                            red_text,
                        )
                    else:
                        worksheet.write(k, 0, j.name, center_text)
                        worksheet.write(k, 1, j.sh_account, center_text)
                        worksheet.write(
                            k, 2, str(j.sh_due_customer_invoice_date), center_text
                        )
                        if j.sh_due_customer_due_date:
                            worksheet.write(
                                k, 3, str(j.sh_due_customer_due_date), center_text
                            )
                        else:
                            worksheet.write(k, 3, "", center_text)
                        worksheet.write(
                            k,
                            4,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_due_customer_amount)),
                            center_text,
                        )
                        worksheet.write(
                            k,
                            5,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_due_customer_paid_amount)),
                            center_text,
                        )
                        worksheet.write(
                            k,
                            6,
                            str(i.currency_id.symbol)
                            + str("{:.2f}".format(j.sh_due_customer_balance)),
                            center_text,
                        )
                    k = k + 1
                total_amount = total_amount + j.sh_due_customer_amount
                total_paid_amount = total_paid_amount + j.sh_due_customer_paid_amount
                total_balance = total_balance + j.sh_due_customer_balance
        if self.sh_customer_due_statement_ids:
            worksheet.write(k, 4, str("{:.2f}".format(total_amount)), bold_center)
            worksheet.row(k).height = 350
            worksheet.write(k, 5, str("{:.2f}".format(total_paid_amount)), bold_center)
            worksheet.write(k, 6, str("{:.2f}".format(total_balance)), bold_center)

        fp = io.BytesIO()
        workbook.save(fp)

        data = base64.encodebytes(fp.getvalue())
        IrAttachment = self.env["ir.attachment"]
        attachment_vals = {
            "name": "Customer Overdue Statement.xls",
            "res_model": "ir.ui.view",
            "type": "binary",
            "datas": data,
            "public": True,
        }
        fp.close()

        attachment = IrAttachment.search(
            [
                ("name", "=", "Customer Overdue Statement"),
                ("type", "=", "binary"),
                ("res_model", "=", "ir.ui.view"),
            ],
            limit=1,
        )
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = IrAttachment.create(attachment_vals)
        # TODO: make user error here
        if not attachment:
            raise UserError("There is no attachments...")

        url = "/web/content/" + str(attachment.id) + "?download=true"
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "current",
        }

    @api.model
    def _run_auto_send_customer_statements(self):
        temp = []
        statement_partners_ids = (
            self.env["sh.customer.statement.config"].sudo().search([])
        )
        if statement_partners_ids:
            for statement in statement_partners_ids:
                for partner in statement.sh_partner_ids:
                    if partner.id not in temp:
                        temp.append(partner.id)
        partner_ids = self.env["res.partner"].sudo().search([("id", "not in", temp)])
        for partner in partner_ids:
            try:
                # for customer
                if partner.customer_rank > 0:
                    # for statement
                    if not partner.sh_dont_send_customer_statement_auto:
                        if (
                            self.env.company.sh_customer_statement_auto_send
                            and partner.sh_customer_statement_ids
                        ):
                            if self.env.company.filter_only_unpaid_and_send_that and not partner.sh_customer_statement_ids.filtered(lambda x:x.sh_customer_balance > 0):
                                return

                            if self.env.company.sh_customer_statement_action == "daily":
                                if self.env.company.sh_cus_daily_statement_template_id:
                                    mail = self.env.company.sh_cus_daily_statement_template_id.sudo().send_mail(
                                        partner.id, force_send=True
                                    )
                                    mail_id = self.env["mail.mail"].sudo().browse(mail)
                                    if (
                                        mail_id
                                        and self.env.company.sh_cust_create_log_history
                                    ):
                                        self.env[
                                            "sh.customer.mail.history"
                                        ].sudo().create(
                                            {
                                                "name": "Customer Account Statement",
                                                "sh_statement_type": "customer_statement",
                                                "sh_current_date": fields.Datetime.now(),
                                                "sh_partner_id": partner.id,
                                                "sh_mail_id": mail_id.id,
                                                "sh_mail_status": mail_id.state,
                                            }
                                        )
                            elif (
                                self.env.company.sh_customer_statement_action
                                == "weekly"
                            ):
                                today = fields.Date.today().weekday()
                                if int(self.env.company.sh_cust_week_day) == today:
                                    if (
                                        self.env.company.sh_cust_weekly_statement_template_id
                                    ):
                                        mail = self.env.company.sh_cust_weekly_statement_template_id.sudo().send_mail(
                                            partner.id, force_send=True
                                        )
                                        mail_id = (
                                            self.env["mail.mail"].sudo().browse(mail)
                                        )
                                        if (
                                            mail_id
                                            and self.env.company.sh_cust_create_log_history
                                        ):
                                            self.env[
                                                "sh.customer.mail.history"
                                            ].sudo().create(
                                                {
                                                    "name": "Customer Account Statement",
                                                    "sh_statement_type": "customer_statement",
                                                    "sh_current_date": fields.Datetime.now(),
                                                    "sh_partner_id": partner.id,
                                                    "sh_mail_id": mail_id.id,
                                                    "sh_mail_status": mail_id.state,
                                                }
                                            )
                            elif (
                                self.env.company.sh_customer_statement_action
                                == "monthly"
                            ):
                                monthly_day = self.env.company.sh_cust_monthly_date
                                today = fields.Date.today()
                                today_date = today.day
                                if self.env.company.sh_cust_monthly_end:
                                    last_day = calendar.monthrange(
                                        today.year, today.month
                                    )[1]
                                    if today_date == last_day:
                                        if self.env.company.sh_cust_monthly_template_id:
                                            mail = self.env.company.sh_cust_monthly_template_id.sudo().send_mail(
                                                partner.id, force_send=True
                                            )
                                            mail_id = (
                                                self.env["mail.mail"]
                                                .sudo()
                                                .browse(mail)
                                            )
                                            if (
                                                mail_id
                                                and self.env.company.sh_cust_create_log_history
                                            ):
                                                self.env[
                                                    "sh.customer.mail.history"
                                                ].sudo().create(
                                                    {
                                                        "name": "Customer Account Statement",
                                                        "sh_statement_type": "customer_statement",
                                                        "sh_current_date": fields.Datetime.now(),
                                                        "sh_partner_id": partner.id,
                                                        "sh_mail_id": mail_id.id,
                                                        "sh_mail_status": mail_id.state,
                                                    }
                                                )
                                else:
                                    if today_date == monthly_day:
                                        if self.env.company.sh_cust_monthly_template_id:
                                            mail = self.env.company.sh_cust_monthly_template_id.sudo().send_mail(
                                                partner.id, force_send=True
                                            )
                                            mail_id = (
                                                self.env["mail.mail"]
                                                .sudo()
                                                .browse(mail)
                                            )
                                            if (
                                                mail_id
                                                and self.env.company.sh_cust_create_log_history
                                            ):
                                                self.env[
                                                    "sh.customer.mail.history"
                                                ].sudo().create(
                                                    {
                                                        "name": "Customer Account Statement",
                                                        "sh_statement_type": "customer_statement",
                                                        "sh_current_date": fields.Datetime.now(),
                                                        "sh_partner_id": partner.id,
                                                        "sh_mail_id": mail_id.id,
                                                        "sh_mail_status": mail_id.state,
                                                    }
                                                )
                            elif (
                                self.env.company.sh_customer_statement_action
                                == "yearly"
                            ):
                                today = fields.Date.today()
                                today_date = today.day
                                today_month = today.strftime("%B").lower()
                                if (
                                    self.env.company.sh_cust_yearly_date == today_date
                                    and self.env.company.sh_cust_yearly_month
                                    == today_month
                                ):
                                    if self.env.company.sh_cust_yearly_template_id:
                                        mail = self.env.company.sh_cust_yearly_template_id.sudo().send_mail(
                                            partner.id, force_send=True
                                        )
                                        mail_id = (
                                            self.env["mail.mail"].sudo().browse(mail)
                                        )
                                        if (
                                            mail_id
                                            and self.env.company.sh_cust_create_log_history
                                        ):
                                            self.env[
                                                "sh.customer.mail.history"
                                            ].sudo().create(
                                                {
                                                    "name": "Customer Account Statement",
                                                    "sh_statement_type": "customer_statement",
                                                    "sh_current_date": fields.Datetime.now(),
                                                    "sh_partner_id": partner.id,
                                                    "sh_mail_id": mail_id.id,
                                                    "sh_mail_status": mail_id.state,
                                                }
                                            )
                    # for overdue statement
                    if not partner.sh_dont_send_due_customer_statement_auto:
                        if (
                            self.env.company.sh_customer_due_statement_auto_send
                            and partner.sh_customer_due_statement_ids
                        ):
                            if self.env.company.filter_only_unpaid_and_send_that and not partner.sh_customer_due_statement_ids.filtered(lambda x:x.sh_due_customer_balance > 0):
                                return

                            if (
                                self.env.company.sh_customer_due_statement_action
                                == "daily"
                            ):
                                if (
                                    self.env.company.sh_cus_due_daily_statement_template_id
                                ):
                                    mail = self.env.company.sh_cus_due_daily_statement_template_id.sudo().send_mail(
                                        partner.id, force_send=True
                                    )
                                    mail_id = self.env["mail.mail"].sudo().browse(mail)
                                    if (
                                        mail_id
                                        and self.env.company.sh_cust_due_create_log_history
                                    ):
                                        self.env[
                                            "sh.customer.mail.history"
                                        ].sudo().create(
                                            {
                                                "name": "Customer Account Overdue Statement",
                                                "sh_statement_type": "customer_overdue_statement",
                                                "sh_current_date": fields.Datetime.now(),
                                                "sh_partner_id": partner.id,
                                                "sh_mail_id": mail_id.id,
                                                "sh_mail_status": mail_id.state,
                                            }
                                        )
                            elif (
                                self.env.company.sh_customer_due_statement_action
                                == "weekly"
                            ):
                                today = fields.Date.today().weekday()
                                if int(self.env.company.sh_cust_due_week_day) == today:
                                    if (
                                        self.env.company.sh_cust_due_weekly_statement_template_id
                                    ):
                                        mail = self.env.company.sh_cust_due_weekly_statement_template_id.sudo().send_mail(
                                            partner.id, force_send=True
                                        )
                                        mail_id = (
                                            self.env["mail.mail"].sudo().browse(mail)
                                        )
                                        if (
                                            mail_id
                                            and self.env.company.sh_cust_due_create_log_history
                                        ):
                                            self.env[
                                                "sh.customer.mail.history"
                                            ].sudo().create(
                                                {
                                                    "name": "Customer Account Overdue Statement",
                                                    "sh_statement_type": "customer_overdue_statement",
                                                    "sh_current_date": fields.Datetime.now(),
                                                    "sh_partner_id": partner.id,
                                                    "sh_mail_id": mail_id.id,
                                                    "sh_mail_status": mail_id.state,
                                                }
                                            )
                            elif (
                                self.env.company.sh_customer_due_statement_action
                                == "monthly"
                            ):
                                monthly_day = self.env.company.sh_cust_due_monthly_date
                                today = fields.Date.today()
                                today_date = today.day
                                if self.env.company.sh_cust_due_monthly_end:
                                    last_day = calendar.monthrange(
                                        today.year, today.month
                                    )[1]
                                    if today_date == last_day:
                                        if (
                                            self.env.company.sh_cust_due_monthly_template_id
                                        ):
                                            mail = self.env.company.sh_cust_due_monthly_template_id.sudo().send_mail(
                                                partner.id, force_send=True
                                            )
                                            mail_id = (
                                                self.env["mail.mail"]
                                                .sudo()
                                                .browse(mail)
                                            )
                                            if (
                                                mail_id
                                                and self.env.company.sh_cust_due_create_log_history
                                            ):
                                                self.env[
                                                    "sh.customer.mail.history"
                                                ].sudo().create(
                                                    {
                                                        "name": "Customer Account Overdue Statement",
                                                        "sh_statement_type": "customer_overdue_statement",
                                                        "sh_current_date": fields.Datetime.now(),
                                                        "sh_partner_id": partner.id,
                                                        "sh_mail_id": mail_id.id,
                                                        "sh_mail_status": mail_id.state,
                                                    }
                                                )
                                else:
                                    if today_date == monthly_day:
                                        if (
                                            self.env.company.sh_cust_due_monthly_template_id
                                        ):
                                            mail = self.env.company.sh_cust_due_monthly_template_id.sudo().send_mail(
                                                partner.id, force_send=True
                                            )
                                            mail_id = (
                                                self.env["mail.mail"]
                                                .sudo()
                                                .browse(mail)
                                            )
                                            if (
                                                mail_id
                                                and self.env.company.sh_cust_due_create_log_history
                                            ):
                                                self.env[
                                                    "sh.customer.mail.history"
                                                ].sudo().create(
                                                    {
                                                        "name": "Customer Account Overdue Statement",
                                                        "sh_statement_type": "customer_overdue_statement",
                                                        "sh_current_date": fields.Datetime.now(),
                                                        "sh_partner_id": partner.id,
                                                        "sh_mail_id": mail_id.id,
                                                        "sh_mail_status": mail_id.state,
                                                    }
                                                )

                            elif (
                                self.env.company.sh_customer_due_statement_action
                                == "yearly"
                            ):
                                today = fields.Date.today()
                                today_date = today.day
                                today_month = today.strftime("%B").lower()
                                if (
                                    self.env.company.sh_cust_due_yearly_date
                                    == today_date
                                    and self.env.company.sh_cust_due_yearly_month
                                    == today_month
                                ):
                                    if self.env.company.sh_cust_due_yearly_template_id:
                                        mail = self.env.company.sh_cust_due_yearly_template_id.sudo().send_mail(
                                            partner.id, force_send=True
                                        )
                                        mail_id = (
                                            self.env["mail.mail"].sudo().browse(mail)
                                        )
                                        if (
                                            mail_id
                                            and self.env.company.sh_cust_due_create_log_history
                                        ):
                                            self.env[
                                                "sh.customer.mail.history"
                                            ].sudo().create(
                                                {
                                                    "name": "Customer Account Overdue Statement",
                                                    "sh_statement_type": "customer_overdue_statement",
                                                    "sh_current_date": fields.Datetime.now(),
                                                    "sh_partner_id": partner.id,
                                                    "sh_mail_id": mail_id.id,
                                                    "sh_mail_status": mail_id.state,
                                                }
                                            )
            except Exception as e:
                _logger.error("%s", e)


class FilterCustomerStateMent(models.Model):
    _name = "sh.res.partner.filter.statement"
    _description = "Filter Customer Statement"

    partner_id = fields.Many2one("res.partner", "Partner")
    name = fields.Char("Invoice Number")
    currency_id = fields.Many2one("res.currency", "Currency")
    sh_account = fields.Char("Account")
    sh_filter_invoice_date = fields.Date("Invoice Date")
    sh_filter_due_date = fields.Date("Invoice Due Date")
    sh_filter_amount = fields.Monetary("Total Amount")
    sh_filter_paid_amount = fields.Monetary("Paid Amount")
    sh_filter_balance = fields.Monetary("Balance")


class CustomerStateMent(models.Model):
    _name = "sh.customer.statement"
    _description = "Customer Statement"

    partner_id = fields.Many2one("res.partner", "Partner")
    currency_id = fields.Many2one("res.currency", "Currency")
    name = fields.Char("Invoice Number")
    sh_account = fields.Char("Account")
    sh_customer_invoice_date = fields.Date("Invoice Date")
    sh_customer_due_date = fields.Date("Invoice Due Date")
    sh_customer_amount = fields.Monetary("Total Amount")
    sh_customer_paid_amount = fields.Monetary("Paid Amount")
    sh_customer_balance = fields.Monetary("Balance")


class CustomerDueStateMent(models.Model):
    _name = "sh.customer.due.statement"
    _description = "Customer Due Statement"

    partner_id = fields.Many2one("res.partner", "Partner")
    name = fields.Char("Invoice Number")
    currency_id = fields.Many2one("res.currency", "Currency")
    sh_account = fields.Char("Account")
    sh_today = fields.Date("Today")
    sh_due_customer_invoice_date = fields.Date("Invoice Date")
    sh_due_customer_due_date = fields.Date("Invoice Due Date")
    sh_due_customer_amount = fields.Monetary("Total Amount")
    sh_due_customer_paid_amount = fields.Monetary("Paid Amount")
    sh_due_customer_balance = fields.Monetary("Balance")