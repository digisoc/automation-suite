///////////////////////////////////////////////////////
//           Google Form to Discord Webhook          //
// https://github.com/axieax/google-forms-to-discord //
///////////////////////////////////////////////////////

// NOTE: this version has been adapted for extra DigiSoc functionality,
// automating the creation of registration and attendance forms as well

// NOTE: for the most up to date version, see https://github.com/axieax/google-forms-to-discord

/*
  SETUP OPTIONS
*/

// [TODO]: Paste your Discord Webhook URL in the quotation marks below (don't remove the quotation marks)
const webhookURL = "";
// [OPTIONAL]: If you want your responses to be hidden in the notification, change false to true below
const hideResponses = false;
// [OPTIONAL]: If you want to show incomplete rows for grids and checkbox grids, change true to false below
const hideEmptyRows = true;
// Further setup instructions can be found at https://github.com/axieax/google-forms-to-discord/

/*
  DIGISOC SETUP OPTIONS
*/

// [TODO]: Paste the ID of the Google Drive folder for storing forms and responses (https://drive.google.com/drive/folders/[driveID])
const driveID = "";
// [COMPLETED]: Index of the field containing the event name (0-indexed)
const formEventNameIndex = 4;

/*
  DO NOT MODIFY BELOW
*/

// Discord embed limits
const maxTextLength = 1024;
const maxFields = 25;

// function called on form submit
const submitPost = (e) => {
  // prepare POST request to webhook
  const formTitle = e.source.getTitle() ?? "Untitled Form";
  const embed = {
    title: `✨ ${formTitle} has received a new response!`,
    footer: {
      text: "Google Forms to Discord Automation - https://github.com/axieax",
    },
    color: 16766720,
  };

  // retrieve and unpack data
  const responses = e.response.getItemResponses();
  // format responses if responses are not to be hidden in the webhook
  if (!hideResponses) {
    // extract responses
    const payload = extractResponses(responses);
    // ignore empty responses
    if (!payload.length) return;
    // include responses in payload
    embed.fields = payload;
  }

  // create registration and attendance forms
  const eventName = responses[formEventNameIndex].getResponse();
  const [registrationForm, registrationSheet] =
    createRegistrationForm(eventName);
  const [attendanceForm, attendanceSheet] = createAttendanceForm(eventName);
  const formDetails = `
📝 **Registration Form:**
  - Public URL: <${registrationForm.shortenFormUrl(
    registrationForm.getPublishedUrl()
  )}>
  - Editor URL: <${registrationForm.getEditUrl()}>
  - Responses: <${registrationSheet.getUrl()}>
📝 **Attendance Form**:
  - Public URL: <${attendanceForm.shortenFormUrl(
    attendanceForm.getPublishedUrl()
  )}>
  - Editor URL: <${attendanceForm.getEditUrl()}>
  - Responses: <${attendanceSheet.getUrl()}>
  `;

  // create POST request to webhook
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    payload: JSON.stringify({
      username: "Response Carrier",
      avatar_url:
        "https://github.com/axieax/google-forms-to-discord/blob/main/assets/birb.jpg?raw=true",
      content: formDetails,
      embeds: [embed],
    }),
  };
  UrlFetchApp.fetch(webhookURL, options);
};

// extract responses
const extractResponses = (responses) => {
  // format each response
  const payload = [];
  responses.forEach((response) => {
    const item = response.getItem();
    let resp = response.getResponse();
    let respFmt, questions;

    switch (item.getType()) {
      case FormApp.ItemType.CHECKBOX:
        // display checkbox responses on separate lines
        resp = resp.join("\n");
        break;
      case FormApp.ItemType.FILE_UPLOAD:
        // generate URL for uploaded files
        resp =
          "File(s) uploaded:\n" +
          resp
            .map((fileID) => "https://drive.google.com/open?id=" + fileID)
            .join("\n");
        break;
      case FormApp.ItemType.GRID:
        // display grid responses on separate lines
        respFmt = [];
        questions = item.asGridItem().getRows();
        resp.forEach((answer, index) => {
          // exclude empty responses unless specified otherwise
          if (!hideEmptyRows || answer !== null)
            respFmt.push(
              `${questions[index]}: ${
                Array.isArray(answer) ? answer.join(", ") : answer
              }`
            );
        });
        resp = respFmt.join("\n");
        break;
      case FormApp.ItemType.CHECKBOX_GRID:
        // display grid responses on separate lines
        respFmt = [];
        questions = item.asCheckboxGridItem().getRows();
        resp.forEach((answer, index) => {
          // exclude empty responses unless specified otherwise
          if (!hideEmptyRows || answer !== null)
            respFmt.push(
              `${questions[index]}: ${
                Array.isArray(answer) ? answer.join(", ") : answer
              }`
            );
        });
        resp = respFmt.join("\n");
        break;
      default:
        // short answer, paragraph, multiple choice, linear scale, date, time
        break;
    }

    // ignore empty responses unless specified otherwise
    if (resp)
      payload.push({
        name: item.getTitle(),
        value:
          resp.length <= maxTextLength
            ? resp
            : resp.slice(0, maxTextLength - 3) + "...",
        inline: false,
      });
  });

  // TODO: maxFields
  return payload;
};

/////////////////////////////////////////////////
// Registration and Attendance Form Automation //
/////////////////////////////////////////////////

/*
  Connect to DigiSoc Drive folder
*/
const eventsFolder = DriveApp.getFolderById(driveID);
const moveToDrive = (fileName) => {
  const file = DriveApp.getFilesByName(fileName).next();
  file.moveTo(eventsFolder);
};

/*
  Form utilities
*/

// data validation for form fields
const emailValidation = FormApp.createTextValidation()
  .requireTextIsEmail()
  .build();
const zIDValidation = FormApp.createTextValidation()
  .setHelpText("Please enter a valid zID")
  .requireTextMatchesPattern("[zZ]?\\d{7}")
  .build();

// add default fields (name, email, zID) to a form
const addDefaultFields = (form) => {
  // add name fields
  form.addTextItem().setTitle("First name").setRequired(true);
  form.addTextItem().setTitle("Last name").setRequired(true);
  // add email field
  form
    .addTextItem()
    .setTitle("Email")
    .setValidation(emailValidation)
    .setRequired(true);
  // add zID field
  form
    .addTextItem()
    .setTitle("zID")
    .setValidation(zIDValidation)
    .setRequired(true);
};

// create registration form
const createRegistrationForm = (eventName) => {
  // create and setup new form
  const formName = `${eventName} Registration Form`;
  const form = FormApp.create(formName)
    .setDescription(
      `Please fill in your details below to register for ${eventName}!`
    )
    .setConfirmationMessage(
      "Thanks for registering! We hope to see you at our event!"
    )
    .setAllowResponseEdits(true);
  // add name, email and zID fields to form
  addDefaultFields(form);
  // add degree field
  form.addTextItem().setTitle("Degree").setRequired(true);
  // add year field
  form
    .addMultipleChoiceItem()
    .setTitle("Year")
    .setChoiceValues([
      "1st Year",
      "2nd Year",
      "3rd Year",
      "4th Year",
      "5th Year",
    ])
    .showOtherOption(true)
    .setRequired(true);
  // add Arc member field
  form
    .addMultipleChoiceItem()
    .setTitle("Are you an Arc member?")
    .setChoiceValues([
      "Yes",
      "No",
    ])
    .setRequired(true);

  // connect form to spreadsheet
  const sheetName = `${eventName} Registration Responses`;
  const sheet = SpreadsheetApp.create(sheetName);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());

  // move form and spreadsheet to Drive
  moveToDrive(formName);
  moveToDrive(sheetName);
  return [form, sheet];
};

// create attendance form
const createAttendanceForm = (eventName) => {
  // create and setup new form
  const formName = `${eventName} Attendance Form`;
  const form = FormApp.create(formName)
    .setDescription(
      `Please fill in your details below to confirm your attendance for ${eventName}!`
    )
    .setConfirmationMessage("Thanks for attending our event!")
    .setAllowResponseEdits(true);
  // add name, email and zID fields to form
  addDefaultFields(form);
  // add field for additional questions
  form
    .addTextItem()
    .setTitle("Do you have any questions for our presenter?")
    .setRequired(false);

  // connect form to spreadsheet
  const sheetName = `${eventName} Attendance Responses`;
  const sheet = SpreadsheetApp.create(sheetName);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());

  // move form and spreadsheet to Drive
  moveToDrive(formName);
  moveToDrive(sheetName);
  return [form, sheet];
};

/* Future Features:
Embed Limits (https://discord.com/developers/docs/resources/channel#embed-limits)
  - Embed Title (includes Form Title) - Maximum 256 characters
  - Payload Fields (includes Payload Responses) - Maximum 25 responses can be displayed
  - Field Name (includes Response Question) - Maximum 256 characters
  - Total Characters (includes Embed Title, Field Names, Field Values, Footer Text) - Maximum 6000 characters
      - https://developers.google.com/apps-script/reference/forms/form-response#toprefilledurl
Regex?
Date format
Extend ellipsis
*/
