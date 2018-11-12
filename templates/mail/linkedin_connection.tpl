{% extends "mail/base.tpl" %}

{% block subject %}{{ full_name }} - your connection {{ owner_name }} from LinkedIn invites you to OSU DApp{% endblock %}

{% block header_title %}Your connection {{ owner_name }} invites you to OSU DApp{% endblock %}

{% block html %}
<!-- container_400 -->
<table class="container_400" align="center" width="400" border="0" cellspacing="0" cellpadding="0" style="margin: 0 auto;">
  <tr>
    <td mc:edit="text003" align="center" class="text_color_282828" style="color: #282828; font-size: 15px; line-height: 2; font-weight: 500; font-family: lato, Helvetica, sans-serif; mso-line-height-rule: exactly;">
      <div class="editable-text" style="line-height: 2;">
        <span class="text_container">
          <multiline>
            Hello {{ full_name }},
            {{ owner_name }} joined Open Source University DApp and already started to verify gained certificates, diplomas, skills, and professional expertise.
            By verifying your skills and certificates, you’re building the necessary credibility needed in order the professional opportunities you want to get.
            Your achievements have been presented automatically in a secure maner to businesses searching for candidates with particular experience.
          </multiline>
        </span>
      </div>
    </td>
  </tr>
  <!-- horizontal gap -->
  <tr><td height="50"></td></tr>

  <tr>
    <td align="center">
      <!-- button -->
      <table class="button_bg_color_2ecc71 bg_color_2ecc71" bgcolor="#2ecc71" width="225" height="50" align="center" border="0" cellpadding="0" cellspacing="0" style="background-color:#2ecc71; border-radius:3px;">
        <tr>
          <td mc:edit="text004" align="center" valign="middle" style="color: #ffffff; font-size: 16px; font-weight: 600; font-family: lato, Helvetica, sans-serif; mso-line-height-rule: exactly;" class="text_color_ffffff">
            <div class="editable-text">
              <span class="text_container">
                <multiline>
                  <a href="https://dapp.os.university/#/onboarding" style="text-decoration: none; color: #ffffff;">
                    Don’t wait and join now
                  </a>
                </multiline>
              </span>
            </div>
          </td>
        </tr>
      </table><!-- END button -->
    </td>
  </tr>

  <!-- horizontal gap -->
  <tr><td height="25"></td></tr>

</table><!-- END container_400 -->

{% endblock %}