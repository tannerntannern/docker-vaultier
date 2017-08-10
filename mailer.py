from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.context import Context
from django.template.loader import get_template
from pynliner import Pynliner
from celery.contrib.methods import task_method
from celery import current_app as app
from urlparse import urljoin

import sys
import traceback
import time
import send_mail as mailer


class VaultierMailer(object):
    """
    Vaultier base mailer class. Feel free to override me

    Base usage:
    >>> mailer = VaultierMailer(template='mailer/my_template',
    >>>                         subject='[Vaultier] New folder')
    >>> mailer.add_to('john@doe.org').send()

    Note: pass template name without extension. Plaintext and html
    version should exists side by side
    """

    _to = []
    from_email = None
    subject = None
    template_style = 'mailer/layout.css'
    object = None
    _template = 'mailer/layout'

    def __init__(self, **kwargs):
        self._to = kwargs.get('to', [])
        self.from_email = kwargs.get('from_email',
                                     settings.VAULTIER.get('from_email'))
        self.subject = kwargs.get('subject', self.subject)
        self._template = kwargs.get('template', self._template)
        self.template_style = kwargs.get('template_style', self.template_style)
        self.object = kwargs.get('object')

    @property
    def to(self):
        """
        Return list of email recipients
        """
        try:
            return iter(self._to)
        except TypeError:
            return [self._to]

    def add_to(self, value):
        """
        Add recipient
        """
        if value not in self._to:
            self._to.append(value)
        return self

    @property
    def template_plain(self):
        """
        Return Template instance for plaintext mail

        :return: Template
        """

        return get_template("{}.txt".format(self._template))

    @property
    def template_html(self):
        """
        Return Template instance for plaintext mail

        :return: Template
        """
        return get_template("{}.html".format(self._template))

    def send(self, **kwargs):
        """
        Send an email, base on the template and context given to the address
        in recipients.

        :return: None
        """

        not_used = kwargs.pop('async', True)

        self._send(**kwargs)

    def format_subject(self):
        """
        Hook to format, compile or whatever with subject before send

        :return: string
        """
        return self.subject

    @app.task(filter=task_method)
    def _send(self, **kwargs):
        """
        Actually send email in background

        :return:
        """

        ## Old code that doesn't work
        # context = self._build_context(**kwargs)
        # plain, html = self._render(context)
        # msg = EmailMultiAlternatives(
        #     from_email=self.from_email,
        #     to=self.to,
        #     body=plain,
        #     subject=self.format_subject()
        # )
        #
        # msg.attach_alternative(html, 'text/html')
        # msg.send()

        # Write email to file in case it doesn't go through
        from_email = self.from_email
        to = list(self.to)
        subject = self.format_subject()
        context = self._build_context(**kwargs)
        plain, html = self._render(context)

        f = open("/vaultier_data/email.log", "a")
        f.write("date:\t\t" + time.strftime("%d/%m/%Y %H:%M:%S") + "\nfrom:\t\t" + str(from_email) + "\nto:\t\t" + ", ".join(to) + "\nsubject:\t" + str(subject) + "\n\n")
        f.write(plain)
        f.write("\n-------------------------------------------------------------------------\n")
        f.close()

        # Attempt sending email through custom script
        try:
            mailer.send_mail(from_email, to, subject, plain, html)
        except:
            fe = open("/vaultier_data/email_errors.log", "a")
            fe.write(time.strftime("%d/%m/%Y %H:%M:%S") + "\n\n" + str(traceback.format_exc()))
            fe.write("\n-------------------------------------------------------------------------\n")
            fe.close()

    def _render(self, context):
        """
        Renders the plain and html versions of a template.
        Return both in a tuple, where the first element is the plain text
        version and the second element is the html version
        :return: (str, str,)
        """
        if not context:
            context = Context({})

        plain = self.template_plain.render(context)
        html = self.template_html.render(context)
        css = get_template(self.template_style).render(Context({}))

        p = Pynliner()
        html = p.from_string(html).with_cssString(css).run()

        return plain, html

    def _build_context(self, **kwargs):
        """
        Must return an instance of django.template.context.Context
        with the template variables set for each implementation
        :return: None
        """
        # adding full url to logo
        kwargs.update({
            'logo_url': "{}vaultier/images/logo-email.png".format(
                urljoin(settings.SITE_URL, settings.STATIC_URL))
        })
        return Context(kwargs)