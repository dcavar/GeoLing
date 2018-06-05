goog.provide('ol.source.WMTS');
goog.provide('ol.source.WMTSRequestEncoding');

goog.require('goog.array');
goog.require('goog.asserts');
goog.require('goog.math');
goog.require('goog.object');
goog.require('goog.string');
goog.require('goog.uri.utils');
goog.require('ol.TileUrlFunction');
goog.require('ol.TileUrlFunctionType');
goog.require('ol.extent');
goog.require('ol.proj');
goog.require('ol.source.TileImage');
goog.require('ol.tilecoord');
goog.require('ol.tilegrid.WMTS');


/**
 * Request encoding. One of 'KVP', 'REST'.
 * @enum {string}
 * @api
 */
ol.source.WMTSRequestEncoding = {
  KVP: 'KVP',  // see spec §8
  REST: 'REST' // see spec §10
};



/**
 * @classdesc
 * Layer source for tile data from WMTS servers.
 *
 * @constructor
 * @extends {ol.source.TileImage}
 * @param {olx.source.WMTSOptions} options WMTS options.
 * @api
 */
ol.source.WMTS = function(options) {

  // TODO: add support for TileMatrixLimits

  /**
   * @private
   * @type {string}
   */
  this.version_ = goog.isDef(options.version) ? options.version : '1.0.0';

  /**
   * @private
   * @type {string}
   */
  this.format_ = goog.isDef(options.format) ? options.format : 'image/jpeg';

  /**
   * @private
   * @type {Object}
   */
  this.dimensions_ = goog.isDef(options.dimensions) ? options.dimensions : {};

  /**
   * @private
   * @type {string}
   */
  this.coordKeyPrefix_ = '';
  this.resetCoordKeyPrefix_();

  /**
   * @private
   * @type {string}
   */
  this.layer_ = options.layer;

  /**
   * @private
   * @type {string}
   */
  this.matrixSet_ = options.matrixSet;

  /**
   * @private
   * @type {string}
   */
  this.style_ = options.style;

  // FIXME: should we guess this requestEncoding from options.url(s)
  //        structure? that would mean KVP only if a template is not provided.
  var requestEncoding = goog.isDef(options.requestEncoding) ?
      /** @type {ol.source.WMTSRequestEncoding} */ (options.requestEncoding) :
      ol.source.WMTSRequestEncoding.KVP;

  // FIXME: should we create a default tileGrid?
  // we could issue a getCapabilities xhr to retrieve missing configuration
  var tileGrid = options.tileGrid;

  // context property names are lower case to allow for a case insensitive
  // replacement as some services use different naming conventions
  var context = {
    'layer': this.layer_,
    'style': this.style_,
    'tilematrixset': this.matrixSet_
  };

  if (requestEncoding == ol.source.WMTSRequestEncoding.KVP) {
    goog.object.extend(context, {
      'Service': 'WMTS',
      'Request': 'GetTile',
      'Version': this.version_,
      'Format': this.format_
    });
  }

  var dimensions = this.dimensions_;

  /**
   * @param {string} template Template.
   * @return {ol.TileUrlFunctionType} Tile URL function.
   */
  function createFromWMTSTemplate(template) {

    // TODO: we may want to create our own appendParams function so that params
    // order conforms to wmts spec guidance, and so that we can avoid to escape
    // special template params

    template = (requestEncoding == ol.source.WMTSRequestEncoding.KVP) ?
        goog.uri.utils.appendParamsFromMap(template, context) :
        template.replace(/\{(\w+?)\}/g, function(m, p) {
          return (p.toLowerCase() in context) ? context[p.toLowerCase()] : m;
        });

    return (
        /**
         * @param {ol.TileCoord} tileCoord Tile coordinate.
         * @param {number} pixelRatio Pixel ratio.
         * @param {ol.proj.Projection} projection Projection.
         * @return {string|undefined} Tile URL.
         */
        function(tileCoord, pixelRatio, projection) {
          if (goog.isNull(tileCoord)) {
            return undefined;
          } else {
            var localContext = {
              'TileMatrix': tileGrid.getMatrixId(tileCoord[0]),
              'TileCol': tileCoord[1],
              'TileRow': tileCoord[2]
            };
            goog.object.extend(localContext, dimensions);
            var url = template;
            if (requestEncoding == ol.source.WMTSRequestEncoding.KVP) {
              url = goog.uri.utils.appendParamsFromMap(url, localContext);
            } else {
              url = url.replace(/\{(\w+?)\}/g, function(m, p) {
                return localContext[p];
              });
            }
            return url;
          }
        });
  }

  var tileUrlFunction = ol.TileUrlFunction.nullTileUrlFunction;
  var urls = options.urls;
  if (!goog.isDef(urls) && goog.isDef(options.url)) {
    urls = ol.TileUrlFunction.expandUrl(options.url);
  }
  if (goog.isDef(urls)) {
    tileUrlFunction = ol.TileUrlFunction.createFromTileUrlFunctions(
        goog.array.map(urls, createFromWMTSTemplate));
  }

  var tmpExtent = ol.extent.createEmpty();
  var tmpTileCoord = [0, 0, 0];
  tileUrlFunction = ol.TileUrlFunction.withTileCoordTransform(
      /**
       * @param {ol.TileCoord} tileCoord Tile coordinate.
       * @param {ol.proj.Projection} projection Projection.
       * @param {ol.TileCoord=} opt_tileCoord Tile coordinate.
       * @return {ol.TileCoord} Tile coordinate.
       */
      function(tileCoord, projection, opt_tileCoord) {
        goog.asserts.assert(!goog.isNull(tileGrid));
        if (tileGrid.getResolutions().length <= tileCoord[0]) {
          return null;
        }
        var x = tileCoord[1];
        var y = -tileCoord[2] - 1;
        var tileExtent = tileGrid.getTileCoordExtent(tileCoord, tmpExtent);
        var extent = projection.getExtent();

        if (!goog.isNull(extent) && projection.isGlobal()) {
          var numCols = Math.ceil(
              ol.extent.getWidth(extent) /
              ol.extent.getWidth(tileExtent));
          x = goog.math.modulo(x, numCols);
          tmpTileCoord[0] = tileCoord[0];
          tmpTileCoord[1] = x;
          tmpTileCoord[2] = tileCoord[2];
          tileExtent = tileGrid.getTileCoordExtent(tmpTileCoord, tmpExtent);
        }
        if (!ol.extent.intersects(tileExtent, extent) ||
            ol.extent.touches(tileExtent, extent)) {
          return null;
        }
        return ol.tilecoord.createOrUpdate(tileCoord[0], x, y, opt_tileCoord);
      },
      tileUrlFunction);

  goog.base(this, {
    attributions: options.attributions,
    crossOrigin: options.crossOrigin,
    logo: options.logo,
    projection: options.projection,
    tileClass: options.tileClass,
    tileGrid: tileGrid,
    tileLoadFunction: options.tileLoadFunction,
    tilePixelRatio: options.tilePixelRatio,
    tileUrlFunction: tileUrlFunction
  });

};
goog.inherits(ol.source.WMTS, ol.source.TileImage);


/**
 * Get the dimensions, i.e. those passed to the constructor through the
 * "dimensions" option, and possibly updated using the updateDimensions
 * method.
 * @return {Object} Dimensions.
 * @api
 */
ol.source.WMTS.prototype.getDimensions = function() {
  return this.dimensions_;
};


/**
 * @return {string} Format.
 * @api
 */
ol.source.WMTS.prototype.getFormat = function() {
  return this.format_;
};


/**
 * @inheritDoc
 */
ol.source.WMTS.prototype.getKeyZXY = function(z, x, y) {
  return this.coordKeyPrefix_ + goog.base(this, 'getKeyZXY', z, x, y);
};


/**
 * @return {string} Layer.
 * @api
 */
ol.source.WMTS.prototype.getLayer = function() {
  return this.layer_;
};


/**
 * @return {string} MatrixSet.
 * @api
 */
ol.source.WMTS.prototype.getMatrixSet = function() {
  return this.matrixSet_;
};


/**
 * @return {string} Style.
 * @api
 */
ol.source.WMTS.prototype.getStyle = function() {
  return this.style_;
};


/**
 * @return {string} Version.
 * @api
 */
ol.source.WMTS.prototype.getVersion = function() {
  return this.version_;
};


/**
 * @private
 */
ol.source.WMTS.prototype.resetCoordKeyPrefix_ = function() {
  var i = 0;
  var res = [];
  for (var key in this.dimensions_) {
    res[i++] = key + '-' + this.dimensions_[key];
  }
  this.coordKeyPrefix_ = res.join('/');
};


/**
 * Update the dimensions.
 * @param {Object} dimensions Dimensions.
 * @api
 */
ol.source.WMTS.prototype.updateDimensions = function(dimensions) {
  goog.object.extend(this.dimensions_, dimensions);
  this.resetCoordKeyPrefix_();
  this.changed();
};


/**
 * @param {Object} wmtsCap An object representing the capabilities document.
 * @param {Object} config Configuration properties for the layer.  Defaults for
 *                  the layer will apply if not provided.
 *
 * Required config properties:
 * layer - {String} The layer identifier.
 *
 * Optional config properties:
 * matrixSet - {String} The matrix set identifier, required if there is
 *      more than one matrix set in the layer capabilities.
 * projection - {String} The desired CRS when no matrixSet is specified.
 *     eg: "EPSG:3857". If the desired projection is not available,
 *     an error is thrown.
 * requestEncoding - {String} url encoding format for the layer. Default is the
 *     first tile url format found in the GetCapabilities response.
 * style - {String} The name of the style
 * format - {String} Image format for the layer. Default is the first
 *     format returned in the GetCapabilities response.
 * @return {olx.source.WMTSOptions} WMTS source options object.
 * @api
 */
ol.source.WMTS.optionsFromCapabilities = function(wmtsCap, config) {

  /* jshint -W069 */

  // TODO: add support for TileMatrixLimits
  goog.asserts.assert(!goog.isNull(config['layer']));

  var layers = wmtsCap['Contents']['Layer'];
  var l = goog.array.find(layers, function(elt, index, array) {
    return elt['Identifier'] == config['layer'];
  });
  goog.asserts.assert(!goog.isNull(l));

  goog.asserts.assert(l['TileMatrixSetLink'].length > 0);
  var idx, matrixSet;
  if (l['TileMatrixSetLink'].length > 1) {
    idx = goog.array.findIndex(l['TileMatrixSetLink'],
        function(elt, index, array) {
          return elt['TileMatrixSet'] == config['matrixSet'];
        });
  } else if (goog.isDef(config['projection'])) {
    idx = goog.array.findIndex(l['TileMatrixSetLink'],
        function(elt, index, array) {
          return elt['TileMatrixSet']['SupportedCRS'].replace(
              /urn:ogc:def:crs:(\w+):(.*:)?(\w+)$/, '$1:$3'
                 ) == config['projection'];
        });
  } else {
    idx = 0;
  }
  if (idx < 0) {
    idx = 0;
  }
  matrixSet = /** @type {string} */
      (l['TileMatrixSetLink'][idx]['TileMatrixSet']);

  goog.asserts.assert(!goog.isNull(matrixSet));

  var format = /** @type {string} */ (l['Format'][0]);
  if (goog.isDef(config['format'])) {
    format = config['format'];
  }
  idx = goog.array.findIndex(l['Style'], function(elt, index, array) {
    if (goog.isDef(config['style'])) {
      return elt['Title'] == config['style'];
    } else {
      return elt['isDefault'];
    }
  });
  if (idx < 0) {
    idx = 0;
  }
  var style = /** @type {string} */ (l['Style'][idx]['Identifier']);

  var dimensions = {};
  if (goog.isDef(l['Dimension'])) {
    goog.array.forEach(l['Dimension'], function(elt, index, array) {
      var key = elt['Identifier'];
      var value = elt['default'];
      if (goog.isDef(value)) {
        goog.asserts.assert(goog.array.contains(elt['values'], value));
      } else {
        value = elt['values'][0];
      }
      goog.asserts.assert(goog.isDef(value));
      dimensions[key] = value;
    });
  }

  var matrixSets = wmtsCap['Contents']['TileMatrixSet'];
  var matrixSetObj = goog.array.find(matrixSets, function(elt, index, array) {
    return elt['Identifier'] == matrixSet;
  });
  goog.asserts.assert(!goog.isNull(matrixSetObj));

  var tileGrid = ol.tilegrid.WMTS.createFromCapabilitiesMatrixSet(
      matrixSetObj);

  var projection;
  if (goog.isDef(config['projection'])) {
    projection = ol.proj.get(config['projection']);
  } else {
    projection = ol.proj.get(matrixSetObj['SupportedCRS'].replace(
        /urn:ogc:def:crs:(\w+):(.*:)?(\w+)$/, '$1:$3'));
  }

  /** @type {!Array.<string>} */
  var urls = [];
  var requestEncoding = config['requestEncoding'];
  requestEncoding = goog.isDef(requestEncoding) ? requestEncoding : '';

  goog.asserts.assert(
      goog.array.contains(['REST', 'RESTful', 'KVP', ''], requestEncoding));

  if (!wmtsCap['OperationsMetadata'].hasOwnProperty('GetTile') ||
      goog.string.startsWith(requestEncoding, 'REST')) {
    // Add REST tile resource url
    requestEncoding = ol.source.WMTSRequestEncoding.REST;
    goog.array.forEach(l['ResourceURL'], function(elt, index, array) {
      if (elt['resourceType'] == 'tile') {
        format = elt['format'];
        urls.push(/** @type {string} */ (elt['template']));
      }
    });
  } else {
    var gets = wmtsCap['OperationsMetadata']['GetTile']['DCP']['HTTP']['Get'];

    var constraint = goog.array.find(gets[0]['Constraint'],
        function(elt, index, array) {
          return elt['name'] == 'GetEncoding';
        });
    var encodings = constraint['AllowedValues']['Value'];
    if (encodings.length > 0 && goog.array.contains(encodings, 'KVP')) {
      requestEncoding = ol.source.WMTSRequestEncoding.KVP;
      urls.push(/** @type {string} */ (gets[0]['href']));

    }
  }
  goog.asserts.assert(urls.length > 0);

  return {
    urls: urls,
    layer: config['layer'],
    matrixSet: matrixSet,
    format: format,
    projection: projection,
    requestEncoding: requestEncoding,
    tileGrid: tileGrid,
    style: style,
    dimensions: dimensions
  };

  /* jshint +W069 */

};
