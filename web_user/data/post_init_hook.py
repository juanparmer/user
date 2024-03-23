import xmlrpc.client

url = 'https://demo5.odoo.com'
db = 'demo_saas-171_fb029eccf102_1709855885'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# web
arch_base = '''<data>
<xpath expr="//t[@t-set='odoo_logo']" position="replace">
    <t t-set="odoo_logo">
        <a target="_blank" t-attf-href="https://d-3system.com.au" class="badge text-bg-light">
            <img alt="Dimension3" src="https://d-3system.com.au/wp-content/uploads/2020/05/Dimension3_Systems_460x159.png" width="62" height="20" style="width: auto; height: 1em; vertical-align: baseline;"/>
        </a>
    </t>
</xpath>
<xpath expr="//t[@t-set='final_message']" position="replace">
    <t t-set="final_message">Designed by %s%s</t>
</xpath>
</data>'''
domain = [('module', '=', 'web'), ('name', '=', 'brand_promotion_message')]
imd = models.execute_kw(
    db, uid, password, 'ir.model.data', 'search_read', [domain])
if not imd:
    print('Unsuccessful!', 'Module web has not been installed')
else:
    [iuv] = models.execute_kw(
        db, uid, password, imd[0]['model'], 'read', [imd[0]['res_id']])
    if iuv.get('inherit_children_ids'):
        print('Successful!', 'web', 'It has already been modified')
    else:
        vals = {
            'model': imd[0]['model'],
            'type': iuv.get('type'),
            'inherit_id': iuv.get('id'),
            'mode': 'extension',
            'arch_base': arch_base
        }
        nimd = models.execute_kw(
            db, uid, password, imd[0]['model'], 'create', [vals])
        print('Successful!', 'web', 'Created: ', nimd)

# website_sale
arch_base = '''<data>
<xpath expr="//t[@t-call='web.brand_promotion_message']" position="replace">
    <t t-call="web.brand_promotion_message">
        <t t-set="_message"></t>
        <t t-set="_utm_medium"></t>
    </t>
</xpath>
</data>'''
domain = [('module', '=', 'website_sale'), ('name', '=', 'brand_promotion')]
imd = models.execute_kw(
    db, uid, password, 'ir.model.data', 'search_read', [domain])
if not imd:
    print('Unsuccessful!', 'Module website_sale has not been installed')
else:
    [iuv] = models.execute_kw(
        db, uid, password, imd[0]['model'], 'read', [imd[0]['res_id']])
    if iuv.get('inherit_children_ids'):
        print('Successful!', 'website_sale', 'It has already been modified')
    else:
        vals = {
            'model': imd[0]['model'],
            'type': iuv.get('type'),
            'inherit_id': iuv.get('id'),
            'mode': 'extension',
            'arch_base': arch_base
        }
        nimd = models.execute_kw(
            db, uid, password, imd[0]['model'], 'create', [vals])
        print('Successful!', 'website_sale', 'Created: ', nimd)

# documents
templates = ['mail_template_document_request_reminder',
             'mail_template_document_request']
for t in templates:
    domain = [('module', '=', 'documents'), ('name', '=', t)]
    imd = models.execute_kw(
        db, uid, password, 'ir.model.data', 'search_read', [domain])
    if not imd:
        print('Unsuccessful!', 'Module documents has not been installed')
    else:
        [mt] = models.execute_kw(
            db, uid, password, imd[0]['model'], 'read', [imd[0]['res_id']])
        r0 = 'Powered by <a target="_blank" href="https://www.odoo.com/app/documents" style="color: #875A7B;">Odoo Documents</a>'
        r1 = '<!-- Powered by <a target="_blank" href="https://www.odoo.com/app/documents" style="color: #875A7B;">Odoo Documents</a> -->'
        if r1 in mt.get('body_html'):
            print('Successful!', 'documents', t,
                  'It Has already been commented')
        else:
            body_html = mt.get('body_html').replace(r0, r1)
            res = models.execute_kw(db, uid, password, imd[0]['model'], 'write', [
                                    mt.get('id'), {'body_html': body_html}])
            print('Successful!', 'documents', t, 'Result: ', res)

# Portal: User Invite
domain = [('module', '=', 'portal'), ('name', '=',
                                      'mail_template_data_portal_welcome')]
imd = models.execute_kw(
    db, uid, password, 'ir.model.data', 'search_read', [domain])
if not imd:
    print('Unsuccessful!', 'Module portal has not been installed')
else:
    [mt] = models.execute_kw(db, uid, password, imd[0]
                             ['model'], 'read', [imd[0]['res_id']])
    r0 = 'Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=portalinvite" style="color: #875A7B;">Odoo</a>'
    r1 = '<!-- Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=portalinvite" style="color: #875A7B;">Odoo</a> -->'
    if r1 in mt.get('body_html'):
        print('Successful!', 'portal', 'It has already been commented')
    else:
        body_html = mt.get('body_html').replace(r0, r1)
        res = models.execute_kw(db, uid, password, imd[0]['model'], 'write', [
                                mt.get('id'), {'body_html': body_html}])
        print('Successful!', 'portal', 'Result: ', res)

# auth_signup
templates = ['set_password_email', 'mail_template_user_signup_account_created']
for t in templates:
    domain = [('module', '=', 'auth_signup'), ('name', '=', t)]
    imd = models.execute_kw(
        db, uid, password, 'ir.model.data', 'search_read', [domain])
    if not imd:
        print('Unsuccessful!', 'Module auth_signup has not been installed')
    else:
        [mt] = models.execute_kw(
            db, uid, password, imd[0]['model'], 'read', [imd[0]['res_id']])
        r0 = 'Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=auth" style="color: #875A7B;">Odoo</a>'
        r1 = '<!-- Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=auth" style="color: #875A7B;">Odoo</a> -->'
        if r1 in mt.get('body_html'):
            print('Successful!', 'auth_signup', t,
                  'It Has already been commented')
        else:
            body_html = mt.get('body_html').replace(r0, r1)
            res = models.execute_kw(db, uid, password, imd[0]['model'], 'write', [
                                    mt.get('id'), {'body_html': body_html}])
            print('Successful!', 'auth_signup', t, 'Result: ', res)

# sale_subscription
templates = ['email_payment_close',
             'email_payment_reminder', 'email_payment_success']
for t in templates:
    domain = [('module', '=', 'sale_subscription'), ('name', '=', t)]
    imd = models.execute_kw(
        db, uid, password, 'ir.model.data', 'search_read', [domain])
    if not imd:
        print('Unsuccessful!', 'Module sale_subscription has not been installed')
    else:
        [mt] = models.execute_kw(
            db, uid, password, imd[0]['model'], 'read', [imd[0]['res_id']])
        r0 = 'Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=mail" style="color: #875A7B;">Odoo</a>'
        r1 = '<!-- Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=mail" style="color: #875A7B;">Odoo</a> -->'
        if r1 in mt.get('body_html'):
            print('Successful!', 'sale_subscription',
                  t, 'It Has already been commented')
        else:
            body_html = mt.get('body_html').replace(r0, r1)
            res = models.execute_kw(db, uid, password, imd[0]['model'], 'write', [
                                    mt.get('id'), {'body_html': body_html}])
            print('Successful!', 'sale_subscription', t, 'Result: ', res)

# timesheet_grid
templates = ['mail_template_timesheet_reminder',
             'mail_template_timesheet_reminder_user']
for t in templates:
    domain = [('module', '=', 'timesheet_grid'), ('name', '=', t)]
    imd = models.execute_kw(
        db, uid, password, 'ir.model.data', 'search_read', [domain])
    if not imd:
        print('Unsuccessful!', 'Module timesheet_grid has not been installed')
    else:
        [mt] = models.execute_kw(
            db, uid, password, imd[0]['model'], 'read', [imd[0]['res_id']])
        r0 = 'Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=mail" style="color: #875A7B;">Odoo</a>'
        r1 = '<!-- Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=mail" style="color: #875A7B;">Odoo</a> -->'
        if r1 in mt.get('body_html'):
            print('Successful!', 'timesheet_grid',
                  t, 'It Has already been commented')
        else:
            body_html = mt.get('body_html').replace(r0, r1)
            res = models.execute_kw(db, uid, password, imd[0]['model'], 'write', [
                                    mt.get('id'), {'body_html': body_html}])
            print('Successful!', 'timesheet_grid', t, 'Result: ', res)

print('Successful!', 'Done')
