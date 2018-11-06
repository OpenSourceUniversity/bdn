{% extends "mail/base.tpl" %}

{% block subject %}Linked In invite{% endblock %}

{% block header_title %}Account Created{% endblock %}

{% block html %}
<!-- container_400 -->
<table class="container_400" align="center" width="400" border="0" cellspacing="0" cellpadding="0" style="margin: 0 auto;">
  <tr>
    <td mc:edit="text003" align="center" class="text_color_282828" style="color: #282828; font-size: 15px; line-height: 2; font-weight: 500; font-family: lato, Helvetica, sans-serif; mso-line-height-rule: exactly;">
      <div class="editable-text" style="line-height: 2;">
        <span class="text_container">
          <multiline>
            Congratulations! Your account has been created and is ready to use.
            Next steps are to confirm your email and follow the link below to start using the platform.
            Before starting with step-by-step instructions please confirm your email.
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
                  <a href="{{ unsubscribe_link }}" style="text-decoration: none; color: #ffffff;">
                    Unsubscribe
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
  <tr><td height="50"></td></tr>

  <tr>
    <td mc:edit="text003" align="center" class="text_color_282828" style="color: #282828; font-size: 15px; line-height: 2; font-weight: 500; font-family: lato, Helvetica, sans-serif; mso-line-height-rule: exactly;">
      <div class="editable-text" style="line-height: 2;">
        <span class="text_container">
          <multiline>
            In case you did not create the account on OS.University, please ignore this email.
          </multiline>
        </span>
      </div>
    </td>
  </tr>

  <!-- horizontal gap -->
  <tr><td height="25"></td></tr>

</table><!-- END container_400 -->

{% endblock %}