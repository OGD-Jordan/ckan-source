/* Arabic Translation for jQuery UI date picker plugin. */
(function (factory) {
  "use strict";
  if (typeof define === "function" && define.amd) {
    define(["../widgets/datepicker"], factory);
  } else {
    factory(jQuery.datepicker);
  }
})(function (datepicker) {
  "use strict";

  // Arabic configuration
  datepicker.regional.ar = {
    closeText: "إغلاق",
    prevText: "السابق",
    nextText: "التالي",
    currentText: "اليوم",
    monthNames: ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
      "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"],
    monthNamesShort: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    dayNames: ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
    dayNamesShort: ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت"],
    dayNamesMin: ["ح", "ن", "ث", "ر", "خ", "ج", "س"],
    weekHeader: "أسبوع",
    dateFormat: 'yy-mm-dd',
    firstDay: 0,
    isRTL: true,
    showMonthAfterYear: false,
    yearSuffix: ""
  };

  // English configuration
  datepicker.regional.en = {
    closeText: "Close",
    prevText: "Prev",
    nextText: "Next",
    currentText: "Today",
    monthNames: ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"],
    monthNamesShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    dayNamesShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    dayNamesMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
    weekHeader: "Wk",
    dateFormat: 'yy-mm-dd',
    firstDay: 0,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ""
  };

  return datepicker.regional.ar;
});

$(document).ready(function () {
  // Initialize all date inputs
  $("input[type=date]").each(function () {
    $(this).datepicker({
      dateFormat: 'yy-mm-dd',
      altField: this,
      changeMonth: true,
      changeYear: true
    });
  });

  // Apply localization based on HTML lang attribute
  const lang = $("html").attr("lang") || "en";
  $("input[type=date]").datepicker("option", $.datepicker.regional[lang]);

});
