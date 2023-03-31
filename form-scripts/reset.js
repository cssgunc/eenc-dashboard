// Run function to reset the database

function reset() {
  // Intializes the environment to get the firestore email, private key, and project ID
  const env = PropertiesService.getScriptProperties().getProperties();

  // Assigns associated value to the correct variable
  const email = env.email;
  const key = env.key;
  const projectId = env.project_id;

  // Intializes a connection to the firestore database
  let firestore = FirestoreApp.getFirestore(email, key, projectId);

  // Gets a reference to the spreadsheet
  let ss = SpreadsheetApp.getActiveSpreadsheet();
  // Gets an array of sheets from the spreadsheet
  let sheets = ss.getSheets();

  // Counter used specifically master database
  let counter = 0;

  // Iterates through each sheet and runs delete command based on number of rows in the sheet
  sheets.forEach((sheet) => {
    let lastRow = sheet.getLastRow() - 1;
    for (let i = 0; i < lastRow; i++) {
      firestore.deleteDocument(sheet.getName() + "/row" + i);
      firestore.deleteDocument("master_data/row" + counter);
      counter += 1;
    }
  });
}
