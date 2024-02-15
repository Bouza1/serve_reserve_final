''' The core of this email template was taken from https://github.com/leemunroe/responsive-html-email-template/blob/master/email.html and then altered and expanded on to meet our needs '''
delete_account_template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>Delete Account Confirmation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style type="text/css">
        @media screen {
            @font-face {
            font-family: 'Source Sans Pro';
            font-style: normal;
            font-weight: 400;
            src: local('Source Sans Pro Regular'), local('SourceSansPro-Regular'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlBM0YzuT7MdOe03otPbuUS0.woff) format('woff');
            }
            @font-face {
            font-family: 'Source Sans Pro';
            font-style: normal;
            font-weight: 700;
            src: local('Source Sans Pro Bold'), local('SourceSansPro-Bold'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/toadOcfmlt9b38dHJxOBGFkQc6VGVFSmCnC_l7QZG60.woff) format('woff');
            }
        }
        body,
        table,
        td,
        a {
            -ms-text-size-adjust: 100%; 
            -webkit-text-size-adjust: 100%; 
        }

        table,
        td {
            mso-table-rspace: 0pt;
            mso-table-lspace: 0pt;
        }

        img {
            -ms-interpolation-mode: bicubic;
        }

        a[x-apple-data-detectors] {
            font-family: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
            color: inherit !important;
            text-decoration: none !important;
        }

        div[style*="margin: 16px 0;"] {
            margin: 0 !important;
        }
        body {
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        table {
            border-collapse: collapse !important;
        }
        a {
            color: #1a82e2;
        }
        img {
            height: auto;
            line-height: 100%;
            text-decoration: none;
            border: 0;
            outline: none;
        }
    </style>
  </head>
  <body style="background-color: #e9ecef;">


    <div class="preheader" style="display: none; max-width: 0; max-height: 0; overflow: hidden; font-size: 1px; line-height: 1px; color: #fff; opacity: 0;">
        Account Deleted.
    </div>

    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
        <td align="center" bgcolor="#1a1a1a">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
            <tr>
                <td align="center" valign="top" style="padding:10px;">
                    <p style="color:#f5f5f5; display: inline; font-size:24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;">Serve <p style="color:#9F9DFF; font-size:24px; display: inline; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;">Reserve</p></p>
                </td>
            </tr>
            </table>

        </td>
        </tr>
        <tr>
        <td align="center" bgcolor="#1E1E1E">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
            <tr>
                <td align="left" bgcolor="#1E1E1E" style="padding: 36px 24px 0; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; border-top: 3px solid #d4dadf;">
                    <h1 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px; color:whitesmoke;">Your Account</h1>
                </td>
            </tr>
            </table>

        </td>
        </tr>
        <tr>
            <td align="center" bgcolor="#e9ecef">
                
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
                <tr>
                    <td align="left" bgcolor="#1E1E1E" style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
                        <p style="margin: 0; color:whitesmoke;"> Your account and all information pertaining to yourselves has been deleted on your behalf.</p>
                    </td>
                </tr>

                <tr>
                    <td align="left" bgcolor="#1E1E1E" style="color:whitesmoke;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                        <td align="center" bgcolor="#1E1E1E" style="padding: 12px;">
                                <table border="0" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td>Username: </td>
                                        <td> $username</td>
                                    </tr>
                                </table>
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>
                <tr>
                    <td align="left" bgcolor="#1E1E1E" style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
                        <p style="margin: 0; color:whitesmoke;">If you did not request your account to be deleted, then please accept our sicerest appologises.</p>
                    </td>
                </tr>
                </table>
                <table style="width:100%; border-top:4px solid whitesmoke;">
                    <tr>
                        <td align="left" bgcolor="#1E1E1E" style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px; border-bottom: 3px solid #d4dadf">
                            <p style="margin: 0; color:whitesmoke">Regards,<br> Serve-Reserve</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        </table>
    </body>
</html>
"""