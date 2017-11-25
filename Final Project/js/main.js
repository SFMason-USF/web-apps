$(function() {
  "use strict";

  /**
   * Shuffle an array in-place
   * @param {Array} array
   */
  function shuffle(array) {
    for (let i = array.length - 1; i > 0; --i) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
  }

  /**
   * URLs.validateLogin: expects a response given the following data:
   * {
   *    newUser: boolean,
   *    email: string,
   *    password: string
   * }
   * The response will be in JSON form with the following fields:
   * {
   *    validEmail: boolean,
   *    validPassword: boolean (optional if validEmail === false),
   *    role: {"student", "instructor"}
   * }
   *
   * URLs.vote: expects simple success notification (TBD) with input data:
   * {
   *    first: id (the site's id as given from the URLs.sites response data),
   *    second: id,
   *    third: id
   * }
   *
   * URLs.votesReport:
   *
   * URLs.sites: expects a response (no input data) in JSON that represents a list of the student sites that have been uploaded to the server in the following form:
   * [
   *    {
   *        url: string (the url for the site's iframe),
   *        id: unique identifier for this site (used to assign ratings to sites)
   *    }
   * ]
   */
  const URLs = Object.freeze({
    validateLogin: "validate-login",
    vote: "vote",
    votesReport: "vote-report",
    sites: "site-list"
  });

  const loginForm = Object.freeze({
    form: $("#login"),
    email: $("#login-email"),
    password: $("#login-password"),
    stayLoggedIn: $("#stay-logged-in")
  });

  $("main.container > div")
    .not("#login-screen")
    .hide();

  //login form functionality
  loginForm.form.submit(function(event) {
    const inputs = $("#login input");
    inputs.prop("disabled", true);

    //Expects json data from the server, containing the user's username, their role
    validateForm(URLs.validateLogin, {
      newUser: false,
      email: loginForm.email.val(),
      password: loginForm.password.val()
    })
      .done(function(data) {
        const loginResponse = JSON.parse(data.responseText);
        switch (false) {
          //if no user found, flag email as wrong
          case loginResponse.validEmail:
            loginForm.email.addClass("has-error");
            break;
          //else if password wrong, flag
          case loginResponse.validPassword:
            loginForm.password.addClass("has-error");
            break;
          //safe to say that login info was good
          default:
            onLogIn(loginResponse);
            break;
        }
      })
      .fail(function(xhr) {
        console.error("Failure!", xhr);
      })
      .always(function() {
        inputs.prop("disabled", false);
      });
  });

  function onLogIn(loginData) {
    $("#login-screen").remove();
    switch (loginResponse.role) {
      case "student":
        $("#student-dashboard").show();
        studentDashInit();
        break;
      case "instructor":
        $("#instructor-dashboard").show();
        break;
      default:
        alert("Error: Unknown user role - " + loginResponse.role);
        break;
    }
  }

  const votes = {
    first: null,
    second: null,
    third: null
  };

  function studentDashInit() {
    $.ajax({
      dataType: "json",
      url: URLs.sites
    }).done(function(response) {
      const siteList = JSON.parse(response.responseText);
      shuffle(siteList);
    });
  }
});
