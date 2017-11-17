"use strict";

/**
  * Validate a form and return the response from the server
  * @param {string} url - The url to send the data to be validated to
  * @param {object} data - The data to validate
  * @returns {jqXHR} - The jqXHR object returned from the ajax request to the server
  */
function validateForm(url, data) {
  return $.ajax({
    async: true,
    data: data,
    method: "POST",
    url: url
  });
}
