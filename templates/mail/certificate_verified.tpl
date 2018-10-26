{% extends "mail/base.tpl" %}

{% block subject %}Open Source University - Certificate {{ certificate_title }} was VERIFIED{% endblock %}

{% block header_title %}Certificate {{ certificate_title }} was VERIFIED{% endblock %}

{% block html %}
<!-- container_400 -->
<table class="container_400" align="center" width="400" border="0" cellspacing="0" cellpadding="0" style="margin: 0 auto;">
  <tr>
    <td mc:edit="text003" align="center" class="text_color_282828" style="color: #282828; font-size: 15px; line-height: 2; font-weight: 500; font-family: lato, Helvetica, sans-serif; mso-line-height-rule: exactly;">
      <div class="editable-text" style="line-height: 2;">
        <span class="text_container">
          <multiline>
            Your certificate {{ certificate_title }} was verified by {{ issuer_name }} and all the skills which are attached to it now are verified.
          </multiline>
        </span>
      </div>
    </td>
  </tr>

  <!-- horizontal gap -->
  <tr><td height="25"></td></tr>

</table><!-- END container_400 -->

{% endblock %}
