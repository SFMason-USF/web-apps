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
   * URLs.votesReport: expects a json object detailing voting records as csv text
   *
   * URLs.siteList: expects a response (no input data) in JSON that represents a list of the student sites that have been uploaded to the server in the following form:
   * [
   *    {
   *        url: string (the url for the site's iframe),
   *        id: unique identifier for this site (used to assign ratings to sites)
   *    }
   * ]
   *
   * URLs.uploadLogins: expects nothing with a csv of login accounts as input
   *
   * URLs.uploadSites: expects nothing with a zip of projects as input
   */
  const URLs = Object.freeze({
    validateLogin: "validate-login",
    vote: "vote",
    votesReport: "vote-report",
    siteList: "site-list",
    uploadLogins: "upload-logins",
    uploadSites: "upload-sites"
  });

  const loginForm = Object.freeze({
    form: $("#login"),
    email: $("#login-email"),
    password: $("#login-password")
  });

  $("main.container > section")
    .not("#login-screen")
    .hide();
  $("#log-out")
    .on("click", function() {
      location.reload();
    })
    .hide();

  //login form functionality
  loginForm.form.submit(function(event) {
    const inputs = $("#login input");
    inputs.prop("disabled", true);

    //Expects json data from the server, containing the user's username, their role
    validateForm(URLs.validateLogin, {
      email: loginForm.email.val(),
      password: loginForm.password.val()
    })
      .done(function(callback) {
        console.log("Callback:", callback);
        // const loginResponse = callback;
        switch (false) {
          //if no user found, flag email as wrong
          case callback.validEmail:
            loginForm.email.addClass("has-error");
            break;
          //else if password wrong, flag
          case callback.validPassword:
            loginForm.password.addClass("has-error");
            break;
          //safe to say that login info was good
          default:
            onLogIn(callback);
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
    $("#log-out").show();
    switch (loginData.role) {
      case "student":
        $("#student-dashboard").show();
        studentDashInit();
        break;
      case "instructor":
        $("#instructor-dashboard").show();
        break;
      default:
        alert("Error: Unknown user role - " + loginData.role);
        break;
    }
  }

  const votes = {
    1: null, //gold medal
    2: null, //silver medal
    3: null, //bronze medal
    //Returns the current rating for siteId, or 0 if it's unranked
    votedOn: function(siteId) {
      for (let i = 1; i <= 3; ++i) {
        if (this[i] == siteId) {
          return i;
        }
      }
      return 0;
    }
  };

  let currentSite = null;

  function studentDashInit() {
    $.ajax({
      dataType: "json",
      url: URLs.siteList
    }).done(function(response) {
      const galleryContainer = $("#sites-gallery");
      console.log("response:", response);
      var siteList = response;
      shuffle(siteList);
      siteList.forEach(function(site, index, list) {
        galleryContainer.append(
          `<div><iframe height="600" name="${site.id}" src="templates/${
            site.url
          }" width="${galleryContainer.css("width")}"></iframe></div>`
        );
      });
      $("#sites-gallery > p.loading").remove();
      galleryContainer.slick({
        onAfterChange: function(slide, index) {
          currentSite = $(slide.$slides.get(index))
            .find("iframe")
            .attr("name");
        }
      });
    });

    $("#rate-first").on("click", function(event) {
      const currentVote = votes.votedOn(currentSite);
      if (currentVote) {
        votes[currentVote] = null;
      }
      votes[1] = currentSite;
    });
    $("#rate-second").on("click", function(event) {
      const currentVote = votes.votedOn(currentSite);
      if (currentVote) {
        votes[currentVote] = null;
      }
      votes[2] = currentSite;
    });
    $("#rate-third").on("click", function(event) {
      const currentVote = votes.votedOn(currentSite);
      if (currentVote) {
        votes[currentVote] = null;
      }
      votes[3] = currentSite;
    });

    $("#submit-votes").on("click", function(event) {
      $.ajax({
        url: URLs.vote,
        method: "POST",
        data: {
          gold: votes[1],
          silver: votes[2],
          bronze: votes[3]
        }
      });
    });
  }

  function instructorDashInit() {
    $("#instructor-dashboard").show();

    // function uploadFile(inputEvent) {
    //   const file = inputEvent.target.files[0];
    //   const reader = new FileReader();
    //   reader.onload = function () {
    //     $.ajax({
    //       url: URLs.uploadLogins,
    //       method: "POST",
    //       data: f
    //     });
    //   };
    //   reader.readAsText(file);
    //   var f = reader.result;
    // }
    // $("#instructor-upload-logins").on("change", function (event) {
    //   var form = $('upload')[1];
    //   var fd = new FormData(form);

    //   $.ajax({
    //     type : 'POST',
    //     url : URLs.uploadLogins,
    //     data: fd,
    //     processData : false,
    //     contentType : false
    //   })
    // });
    // $("#instructor-upload-sites").on("change", function (event) {
    //   uploadFile(event);
    // });
  }
});
