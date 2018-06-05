goog.provide('ol.source.TileArcGISRest');

goog.require('goog.array');
goog.require('goog.asserts');
goog.require('goog.math');
goog.require('goog.object');
goog.require('goog.string');
goog.require('goog.uri.utils');
goog.require('ol');
goog.require('ol.TileCoord');
goog.require('ol.TileUrlFunction');
goog.require('ol.extent');
goog.require('ol.proj');
goog.require('ol.source.TileImage');
goog.require('ol.tilecoord');



/**
 * @classdesc
 * Layer source for tile data from ArcGIS Rest services. Map and Image
 * Services are supported.
 *
 * For cached ArcGIS services, better performance is available using the
 * {@link ol.source.XYZ} data source.
 *
 * @constructor
 * @extends {ol.source.TileImage}
 * @param {olx.source.TileArcGISRestOptions=} opt_options Tile ArcGIS Rest
 *     options.
 * @api
 */
ol.source.TileArcGISRest = function(opt_options) {

  var options = goog.isDef(opt_options) ? opt_options : {};

  var params = goog.isDef(options.params) ? options.params : {};

  goog.base(this, {
    attributions: options.attributions,
    logo: options.logo,
    projection: options.projection,
    tileGrid: options.tileGrid,
    tileLoadFunction: options.tileLoadFunction,
    tileUrlFunction: goog.bind(this.tileUrlFunction_, this)
  });

  var urls = options.urls;
  if (!goog.isDef(urls) && goog.isDef(options.url)) {
    urls = ol.TileUrlFunction.expandUrl(options.url);
  }

  /**
   * @private
   * @type {!Array.<string>}
   */
  this.urls_ = goog.isDefAndNotNull(urls) ? urls : [];

  /**
   * @private
   * @type {Object}
   */
  this.params_ = params;

  /**
   * @private
   * @type {ol.Extent}
   */
  this.tmpExtent_ = ol.extent.createEmpty();

};
goog.inherits(ol.source.TileArcGISRest, ol.source.TileImage);


/**
 * Get the user-provided params, i.e. those passed to the constructor through
 * the "params" option, and possibly updated using the updateParams method.
 * @return {Object} Params.
 * @api
 */
ol.source.TileArcGISRest.prototype.getParams = function() {
  return this.params_;
};


/**
 * @param {ol.TileCoord} tileCoord Tile coordinate.
 * @param {number} tileSize Tile size.
 * @param {ol.Extent} tileExtent Tile extent.
 * @param {number} pixelRatio Pixel ratio.
 * @param {ol.proj.Projection} projection Projection.
 * @param {Object} params Params.
 * @return {string|undefined} Request URL.
 * @private
 */
ol.source.TileArcGISRest.prototype.getRequestUrl_ =
    function(tileCoord, tileSize, tileExtent,
        pixelRatio, projection, params) {

  var urls = this.urls_;
  if (goog.array.isEmpty(urls)) {
    return undefined;
  }

  // ArcGIS Server only wants the numeric portion of the projection ID.
  var srid = projection.getCode().split(':').pop();

  params['SIZE'] = tileSize + ',' + tileSize;
  params['BBOX'] = tileExtent.join(',');
  params['BBOXSR'] = srid;
  params['IMAGESR'] = srid;

  var url;
  if (urls.length == 1) {
    url = urls[0];
  } else {
    var index = goog.math.modulo(ol.tilecoord.hash(tileCoord), urls.length);
    url = urls[index];
  }

  if (!goog.string.endsWith(url, '/')) {
    url = url + '/';
  }

  // If a MapServer, use export. If an ImageServer, use exportImage.
  if (goog.string.endsWith(url, 'MapServer/')) {
    url = url + 'export';
  }
  else if (goog.string.endsWith(url, 'ImageServer/')) {
    url = url + 'exportImage';
  }
  else {
    goog.asserts.fail('Unknown Rest Service', url);
  }

  return goog.uri.utils.appendParamsFromMap(url, params);
};


/**
 * Return the URLs used for this ArcGIS source.
 * @return {!Array.<string>} URLs.
 * @api stable
 */
ol.source.TileArcGISRest.prototype.getUrls = function() {
  return this.urls_;
};


/**
 * @param {string|undefined} url URL.
 * @api stable
 */
ol.source.TileArcGISRest.prototype.setUrl = function(url) {
  var urls = goog.isDef(url) ? ol.TileUrlFunction.expandUrl(url) : null;
  this.setUrls(urls);
};


/**
 * @param {Array.<string>|undefined} urls URLs.
 * @api stable
 */
ol.source.TileArcGISRest.prototype.setUrls = function(urls) {
  this.urls_ = goog.isDefAndNotNull(urls) ? urls : [];
  this.changed();
};


/**
 * @param {ol.TileCoord} tileCoord Tile coordinate.
 * @param {number} pixelRatio Pixel ratio.
 * @param {ol.proj.Projection} projection Projection.
 * @return {string|undefined} Tile URL.
 * @private
 */
ol.source.TileArcGISRest.prototype.tileUrlFunction_ =
    function(tileCoord, pixelRatio, projection) {

  var tileGrid = this.getTileGrid();
  if (goog.isNull(tileGrid)) {
    tileGrid = this.getTileGridForProjection(projection);
  }

  if (tileGrid.getResolutions().length <= tileCoord[0]) {
    return undefined;
  }

  var tileExtent = tileGrid.getTileCoordExtent(
      tileCoord, this.tmpExtent_);
  var tileSize = tileGrid.getTileSize(tileCoord[0]);

  if (pixelRatio != 1) {
    tileSize = (tileSize * pixelRatio + 0.5) | 0;
  }

  // Apply default params and override with user specified values.
  var baseParams = {
    'F': 'image',
    'FORMAT': 'PNG32',
    'TRANSPARENT': true
  };
  goog.object.extend(baseParams, this.params_);

  return this.getRequestUrl_(tileCoord, tileSize, tileExtent,
      pixelRatio, projection, baseParams);
};


/**
 * Update the user-provided params.
 * @param {Object} params Params.
 * @api stable
 */
ol.source.TileArcGISRest.prototype.updateParams = function(params) {
  goog.object.extend(this.params_, params);
  this.changed();
};
