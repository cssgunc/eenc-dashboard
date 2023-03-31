// temporary function to environment variables, so run once and delete

// function temp() {
//   const scriptProperties = PropertiesService.getScriptProperties();
//   scriptProperties.setProperties({
//     email: "insert_email_here",
//     key: "insert_key_here",
//     project_id: "insert_project_id_here",
//   });

//   console.log(PropertiesService.getScriptProperties().getProperties());
// }

/* 
  Intializes the database with all the data currently in your forms
  Only run once or if you reset the database
*/

function intialize() {
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

  // Used for the master database numbering
  let counter = 0;

  // Runs the following code for each sheet, otherwise each form
  sheets.forEach((sheet) => {
    // Following code gets all the column headers and data through row and column numbers
    let lastRow = sheet.getLastRow();
    let lastColumn = sheet.getLastColumn();
    let keyRange = sheet.getRange(1, 1, 1, lastColumn);
    let dataRange = sheet.getRange(2, 1, lastRow - 1, lastColumn);
    let keys = keyRange.getValues()[0];
    let data = dataRange.getValues();

    /* 
      Runs through each row (or each form response) does the associated model creation and
      inserts into the specific form database and master database
    */
    data.forEach((row, index) => {
      // Creates a specific model based the sheet as each form has different questions and number of questions
      const model = createModel(keys);

      // Changes all categorical variables in data to numerical (1 - 5)
      dataCoding(row);

      // Inserts into form specific database
      insertDatabase(row, model, firestore, sheet.getName(), index);

      // Uses object destructuring to get variables we are interested in
      const {
        timestamp,
        course_rating,
        guidelines_before,
        guidelines_after,
        improvement_efforts,
        sharing_interest,
        instructor_rating,
        accessibility_rating,
        navigation_rating,
        current_profession,
        student_count,
        student_location,
      } = model;

      // Creates an object based on the previous model and form name
      const subset = {
        form_name: sheet.getName().toLowerCase().replaceAll(/ /g, "_"),
        timestamp,
        course_rating,
        guidelines_before,
        guidelines_after,
        improvement_efforts,
        sharing_interest,
        instructor_rating,
        accessibility_rating,
        navigation_rating,
        current_profession,
        student_count,
        student_location,
      };

      // Inserts into the aggregated or master database
      insertAggregatedDatabase(subset, firestore, counter, sheet.getName());
      counter += 1;
    });
  });
}

/*
  This function updates the database and is called whenever an attached form is submitted
  The function looks at each forms last row and tries to insert it into the database.
*/

function update() {
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

  // Runs the following code for each sheet, otherwise each form
  sheets.forEach((sheet) => {
    // Following code gets all the column headers and data through row and column numbers
    let lastRow = sheet.getLastRow();
    let lastColumn = sheet.getLastColumn();
    let keyRange = sheet.getRange(1, 1, 1, lastColumn);
    let dataRange = sheet.getRange(lastRow, 1, 1, lastColumn);
    let keys = keyRange.getValues()[0];
    let data = dataRange.getValues()[0];

    // Only creates a singular model and codes a singular row because we are looking at the last row
    const model = createModel(keys);
    dataCoding(data);

    // Tries to insert it into the database and aggregated database but only runs if it is the new form response
    try {
      insertDatabase(data, model, firestore, sheet.getName(), lastRow - 2);

      const {
        timestamp,
        course_rating,
        guidelines_before,
        guidelines_after,
        improvement_efforts,
        sharing_interest,
        instructor_rating,
        accessibility_rating,
        navigation_rating,
        current_profession,
        student_count,
        student_location,
      } = model;

      const subset = {
        form_name: sheet.getName().toLowerCase().replaceAll(/ /g, "_"),
        timestamp,
        course_rating,
        guidelines_before,
        guidelines_after,
        improvement_efforts,
        sharing_interest,
        instructor_rating,
        accessibility_rating,
        navigation_rating,
        current_profession,
        student_count,
        student_location,
      };

      insertAggregatedDatabase(
        subset,
        firestore,
        firestore.getDocuments("master_data").length,
        sheet.getName()
      );
    } catch {
      // Otherwise the error is caught and we log that it is already in the database
      console.log("Already in database");
    }
  });
}

// Function to code categorical variables to numerical and works by interacting the reference so no return value
const dataCoding = (row) => {
  // Runs through every value and if it matches a known category, the value gets coded to a numerical value
  row.forEach((cell, index) => {
    // Firsts standardizes it to lowercase
    if (typeof cell === "string") {
      cell = cell.toLowerCase();
    }

    if (
      cell === "very low" ||
      cell === "not at all interested" ||
      cell === "strongly disagree"
    ) {
      row[index] = 1;
    } else if (
      cell === "low" ||
      cell === "probably not" ||
      cell === "disagree"
    ) {
      row[index] = 2;
    } else if (
      cell === "average" ||
      cell === "potentially interested" ||
      cell === "unsure"
    ) {
      row[index] = 3;
    } else if (
      cell === "high" ||
      cell === "very interested" ||
      cell === "agree"
    ) {
      row[index] = 4;
    } else if (cell == "very high" || cell === "strongly agree") {
      row[index] = 5;
    } else if (cell === "") {
      // Codes any empty values to N/A
      row[index] = "N/A";
    }
  });
};

// Inserts data into the aggregated or master databse
const insertAggregatedDatabase = (data, database, rowNumber, sheet) => {
  const keys = Object.keys(data);

  // Special error handling for Don't Waste It Form as we average the guidelines before and guidelines after
  if (sheet == "TEST Don't Waste It Eval") {
    let before_average = [];
    let after_average = [];

    keys.forEach((key) => {
      if (key.includes("guidelines_after")) {
        before_average.push(data[key]);
      }
      if (key.includes("guidelines_before")) {
        after_average.push(data[key]);
      }
    });

    // Averages and sets the guidelines_before and guidelines_after key to the associated averages
    data["guidelines_before"] =
      before_average.reduce((a, b) => {
        return a + b;
      }) / before_average.length;
    data["guidelines_after"] =
      after_average.reduce((a, b) => {
        return a + b;
      }) / after_average.length;
  }

  // Inserts the document to the master_data database
  database.createDocument("master_data/row" + rowNumber, data);
};

// Inserts data into associated sheet database
const insertDatabase = (row, model, database, sheet, rowNumber) => {
  const keys = Object.keys(model);

  keys.forEach((key, index) => {
    model[key] = row[index];
  });

  // Special error handling for Don't Waste It Form as we average the guidelines before and guidelines after
  if (sheet == "TEST Don't Waste It Eval") {
    let before_average = [];
    let after_average = [];

    keys.forEach((key) => {
      if (key.includes("guidelines_after")) {
        before_average.push(model[key]);
      }
      if (key.includes("guidelines_before")) {
        after_average.push(model[key]);
      }
    });

    // Averages and sets the guidelines_before and guidelines_after key to the associated averages
    model["guidelines_before"] =
      before_average.reduce((a, b) => {
        return a + b;
      }) / before_average.length;
    model["guidelines_after"] =
      after_average.reduce((a, b) => {
        return a + b;
      }) / after_average.length;
  }

  // Inserts the document into the associated sheet database
  database.createDocument(sheet + "/row" + rowNumber, model);
};

//creates a objects (or model) using an array of column
const createModel = (keys) => {
  // uses reduce function and spread operator to make model
  const model = keys.reduce((accumulator, value) => {
    return { ...accumulator, [value]: "" };
  }, {});

  return model;
};
