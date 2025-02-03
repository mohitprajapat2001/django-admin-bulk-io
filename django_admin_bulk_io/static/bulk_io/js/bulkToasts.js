let timer1, timer2;
let toast, closeIcon, progress;

/**
 * * function to add the class to element
 * @param elem element
 * @param class_name class name
 */
const addElemClass = (elem, class_name) => {
  elem.classList.add(class_name);
};

/**
 * function to remove the class from element
 * @param elem element
 * @param class_name class name
 */
const removeElemClass = (elem, class_name) => {
  elem.classList.remove(class_name);
};
/**
 * function to trigger toast message
 * @param toastHeader header of the toast message
 * @param toastBody body of the toast message
 */
const triggerToast = (toastHeader, toastBody) => {
  $(".toast-header").html(toastHeader);
  $(".toast-body").html(toastBody);
  toast.classList.add("active");
  progress.classList.add("active");

  timer1 = setTimeout(() => {
    toast.classList.remove("active");
  }, 5000);

  timer2 = setTimeout(() => {
    progress.classList.remove("active");
  }, 5300);
};

$(document).ready(() => {
  toast = document.querySelector(".toast");
  closeIcon = document.querySelector(".close-toast");
  progress = document.querySelector(".progress");

  closeIcon.addEventListener("click", () => {
    toast.classList.remove("active");
    setTimeout(() => {
      progress.classList.remove("active");
    }, 300);
    clearTimeout(timer1);
    clearTimeout(timer2);
  });
});
