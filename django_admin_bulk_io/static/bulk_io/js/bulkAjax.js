/**
 * function to handle the ajax request to get the data
 * @param url backend url
 * @param callback callback function
 */
const bulkIOGetRequest = (url, callback) => {
  bulkIoAjaxRequest(url, "GET", null, callback);
};
/**
 * function to handle the ajax request to send the data
 * @param url backend url
 * @param data data to send to backend
 * @param callback callback function
 */
const bulkIOPostRequest = (url, data, callback) => {
  bulkIoAjaxRequest(url, "POST", data, callback);
};
/**
 * function to handle the ajax request to send the data
 * @param url backend url
 * @param type request type
 * @param data data to send to backend
 * @param callback callback function
 */
const bulkIoAjaxRequest = (url, type, data, callback) => {
  $.ajax({
    url: url,
    type: type,
    data: data,
    processData: false,
    contentType: false,
    success: (responseData) => {
      responseData && triggerToast("Success", responseData.message);
      callback && callback(responseData);
    },
    error: (error) => {
      console.error(error);
      triggerToast(
        "Error",
        (error.responseJSON && error.responseJSON.message) || error.responseText
      );
    },
  });
};
