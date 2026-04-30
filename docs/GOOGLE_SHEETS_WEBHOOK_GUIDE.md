# Optional Google Sheets Webhook Guide

You can push MathPath chatbot leads into Google Sheets using a simple Google Apps Script webhook.

## Apps Script Example

Create a Google Sheet, then open Extensions > Apps Script and paste this:

```javascript
function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = JSON.parse(e.postData.contents);

  sheet.appendRow([
    data.created_at,
    data.lead_id,
    data.parent_name,
    data.child_name,
    data.child_age,
    data.child_class,
    data.phone,
    data.email,
    data.preferred_mode,
    data.preferred_callback_time,
    data.main_concern,
    data.recommended_program,
    data.lead_score,
    data.lead_priority,
    data.status,
    data.source
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ status: "success" }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

Deploy it as a Web App and set access to allow requests. Then copy the Web App URL into the backend `.env` file:

```env
LEAD_WEBHOOK_URL=https://script.google.com/macros/s/your-deployment-id/exec
```

## Recommended Sheet Header Row

```text
Created At | Lead ID | Parent Name | Child Name | Age | Class | Phone | Email | Preferred Mode | Callback Time | Main Concern | Recommended Program | Lead Score | Priority | Status | Source
```
