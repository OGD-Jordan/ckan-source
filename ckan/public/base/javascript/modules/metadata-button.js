/* Watches the "Show metadata diff" button on the Changes summary page.
 * When the button is pressed, toggles the display of the metadata diff
 * for the chronologically most recent revision on and off.
 *
 * target - a button to watch for changes (default: button)
 *
 */

this.ckan.module('metadata-button', function(jQuery) {
  return {
    options: {
      target: 'button'
    },

    initialize: function () {
      // Watch for our button to be clicked.
      this.el.on('click', jQuery.proxy(this._onClick, this));
    },

    

    _onClick: function(event) {
      let direction = document.documentElement.dir === 'rtl' ? 'rtl' : 'ltr';

      let texts = {
        'ltr': {
          'Show metadata diff': 'Show metadata diff',
          'Hide metadata diff': 'Hide metadata diff'
        },
        'rtl': {
          'Show metadata diff': 'إظهار اختلاف البيانات الوصفية',
          'Hide metadata diff': 'إخفاء اختلاف البيانات الوصفية'
        }
      };
      var div = document.getElementById("metadata_diff");
      div.style.display = (div.style.display === "none") ? "block" : "none";

      var btn = document.getElementById("metadata_button");

      if (btn.value === texts[direction]['Show metadata diff']) {
        btn.value = texts[direction]['Hide metadata diff'];
      } else {
        btn.value = texts[direction]['Show metadata diff'];
      }

    }   
  }
});
