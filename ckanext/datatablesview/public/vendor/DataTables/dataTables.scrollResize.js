/*! ScrollResize for DataTables v1.0.0
 * 2015 SpryMedia Ltd - datatables.net/license
 */
/**
 * @summary     ScrollResize
 * @description Automatically alter the DataTables page length to fit the table
     into a container
 * @version     1.0.0
 * @file        dataTables.scrollResize.js
 * @author      SpryMedia Ltd (www.sprymedia.co.uk)
 * @contact     www.sprymedia.co.uk/contact
 * @copyright   Copyright 2015 SpryMedia Ltd.
 * 
 * License      MIT - http://datatables.net/license/mit
 *
 * This feature plug-in for DataTables will automatically change the DataTables
 * page length in order to fit inside its container. This can be particularly
 * useful for control panels and other interfaces which resize dynamically with
 * the user's browser window instead of scrolling.
 *
 * Page resizing in DataTables can be enabled by using any one of the following
 * options:
 *
 * * Setting the `scrollResize` parameter in the DataTables initialisation to
 *   be true - i.e. `scrollResize: true`
 * * Setting the `scrollResize` parameter to be true in the DataTables
 *   defaults (thus causing all tables to have this feature) - i.e.
 *   `$.fn.dataTable.defaults.scrollResize = true`.
 * * Creating a new instance: `new $.fn.dataTable.ScrollResize( table );` where
 *   `table` is a DataTable's API instance.
 */
!function(t){"function"==typeof define&&define.amd?define(["jquery","datatables.net"],(function(e){return t(e,window,document)})):"object"==typeof exports?module.exports=function(e,o){return e||(e=window),o&&o.fn.dataTable||(o=require("datatables.net")(e,o).$),t(o,e,e.document)}:t(jQuery,window,document)}((function(t,e,o,n){"use strict";var i=function(e){var o=this,n=e.table();this.s={dt:e,host:t(n.container()).parent(),header:t(n.header()),footer:t(n.footer()),body:t(n.body()),container:t(n.container()),table:t(n.node())};var i=this.s.host;"static"===i.css("position")&&i.css("position","relative"),e.on("draw.scrollResize",(function(){o._size()})),e.on("destroy.scrollResize",function(){e.off(".scrollResize"),this.s.obj&&this.s.obj.remove()}.bind(this)),this._attach(),this._size();var a=e.settings()[0],s=a.nScrollBody,r=s.scrollHeight>s.clientHeight;a.scrollBarVis&&!r&&e.columns.adjust()};i.prototype={_size:function(){var e=this.s,o=e.dt.table(),n=t(e.table).offset().top,i=e.host.height(),a=t("div.dataTables_scrollBody",o.container());i-=n,i-=e.container.height()-(n+a.height()),t("div.dataTables_scrollBody",o.container()).css({maxHeight:i,height:i})},_attach:function(){var e=this,o=t("<iframe/>").css({position:"absolute",top:0,left:0,height:"100%",width:"100%",zIndex:-1,border:0}).attr("frameBorder","0").attr("src","about:blank");o[0].onload=function(){var t=this.contentDocument.body,o=t.offsetHeight,n=this.contentDocument;(n.defaultView||n.parentWindow).onresize=function(){var i=t.clientHeight||t.offsetHeight,a=n.documentElement.clientHeight;!i&&a&&(i=a),i!==o&&(o=i,e._size())}},o.appendTo(this.s.host).attr("data","about:blank"),this.s.obj=o}},t.fn.dataTable.ScrollResize=i,t.fn.DataTable.ScrollResize=i,t(o).on("init.dt",(function(e,o){if("dt"===e.namespace){var n=new t.fn.dataTable.Api(o);(o.oInit.scrollResize||t.fn.dataTable.defaults.scrollResize)&&new i(n)}}))}));