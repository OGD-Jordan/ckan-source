this.ckan.module('resource-view-embed', function ($) {
  var modal, self, previewContainer;

  function initialize() {
    self = this;
    modal = $('#embed-' + this.options.id);
    $('body').append(modal);

    previewContainer = $('#embed-preview-container', modal);

    this.el.on('click', _onClick);
    $('textarea', modal).on('focus', _selectAllCode).on('mouseup', _preventClick);
    $('input', modal).on('keyup change', _updateValues);

    $('#predefined-size', modal).on('change', _onSizeChange);

    _updateEmbedCode();

    // Render preview iframe after 1 second
  }
  
  function _onClick(event) {
    event.preventDefault();
    modal.modal('show');
    _renderPreviewIframe();
  }

  function _selectAllCode() {
    $('textarea', modal).select();
  }

  function _updateValues() {
    self.options.width = $('[name="width"]', modal).val();
    self.options.height = $('[name="height"]', modal).val();
    _updateEmbedCode();
    _updatePreviewIframeDimensions();
  }

  function _onSizeChange() {
    const [width, height] = $('#predefined-size', modal).val().split('x');
    $('[name="width"]', modal).val(width);
    $('[name="height"]', modal).val(height);

    self.options.width = width;
    self.options.height = height;

    _updateEmbedCode();
    _updatePreviewIframeDimensions();
  }

  function _updateEmbedCode() {
    $('[name="code"]', modal).val(_embedCode());
  }

  function _preventClick(event) {
    event.preventDefault();
  }

  function _embedCode() {
    return `<iframe title="Data viewer" width="${self.options.width}" height="${self.options.height}" src="${self.options.url}" frameBorder="0"></iframe>`;
  }

  function _renderPreviewIframe() {
    previewContainer.html(_embedCode());
  }

  function _updatePreviewIframeDimensions() {
    const iframe = $('iframe', previewContainer);
    if (iframe.length) {
      iframe.attr('width', self.options.width);
      iframe.attr('height', self.options.height);
    }
  }

  return {
    initialize: initialize,
    options: {
      id: 0,
      url: '#',
      width: 700,
      height: 400
    }
  };
});
