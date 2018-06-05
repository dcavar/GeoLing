goog.provide('ol.interaction.Select');

goog.require('goog.array');
goog.require('goog.asserts');
goog.require('goog.events');
goog.require('goog.events.Event');
goog.require('goog.functions');
goog.require('ol.CollectionEventType');
goog.require('ol.Feature');
goog.require('ol.FeatureOverlay');
goog.require('ol.events.condition');
goog.require('ol.geom.GeometryType');
goog.require('ol.interaction.Interaction');
goog.require('ol.style.Style');


/**
 * @enum {string}
 */
ol.SelectEventType = {
  /**
   * Triggered when feature(s) has been (de)selected.
   * @event ol.SelectEvent#select
   * @api
   */
  SELECT: 'select'
};



/**
 * @classdesc
 * Events emitted by {@link ol.interaction.Select} instances are instances of
 * this type.
 *
 * @param {string} type The event type.
 * @param {Array.<ol.Feature>} selected Selected features.
 * @param {Array.<ol.Feature>} deselected Deselected features.
 * @extends {goog.events.Event}
 * @constructor
 */
ol.SelectEvent = function(type, selected, deselected) {
  goog.base(this, type);

  /**
   * Selected features array.
   * @type {Array.<ol.Feature>}
   * @api
   */
  this.selected = selected;

  /**
   * Deselected features array.
   * @type {Array.<ol.Feature>}
   * @api
   */
  this.deselected = deselected;
};
goog.inherits(ol.SelectEvent, goog.events.Event);



/**
 * @classdesc
 * Handles selection of vector data. A {@link ol.FeatureOverlay} is maintained
 * internally to store the selected feature(s). Which features are selected is
 * determined by the `condition` option, and optionally the `toggle` or
 * `add`/`remove` options.
 *
 * @constructor
 * @extends {ol.interaction.Interaction}
 * @param {olx.interaction.SelectOptions=} opt_options Options.
 * @api stable
 */
ol.interaction.Select = function(opt_options) {

  goog.base(this, {
    handleEvent: ol.interaction.Select.handleEvent
  });

  var options = goog.isDef(opt_options) ? opt_options : {};

  /**
   * @private
   * @type {ol.events.ConditionType}
   */
  this.condition_ = goog.isDef(options.condition) ?
      options.condition : ol.events.condition.singleClick;

  /**
   * @private
   * @type {ol.events.ConditionType}
   */
  this.addCondition_ = goog.isDef(options.addCondition) ?
      options.addCondition : ol.events.condition.never;

  /**
   * @private
   * @type {ol.events.ConditionType}
   */
  this.removeCondition_ = goog.isDef(options.removeCondition) ?
      options.removeCondition : ol.events.condition.never;

  /**
   * @private
   * @type {ol.events.ConditionType}
   */
  this.toggleCondition_ = goog.isDef(options.toggleCondition) ?
      options.toggleCondition : ol.events.condition.shiftKeyOnly;

  /**
   * @private
   * @type {boolean}
   */
  this.multi_ = goog.isDef(options.multi) ? options.multi : false;

  var layerFilter;
  if (goog.isDef(options.layers)) {
    if (goog.isFunction(options.layers)) {
      layerFilter = options.layers;
    } else {
      var layers = options.layers;
      layerFilter =
          /**
           * @param {ol.layer.Layer} layer Layer.
           * @return {boolean} Include.
           */
          function(layer) {
        return goog.array.contains(layers, layer);
      };
    }
  } else {
    layerFilter = goog.functions.TRUE;
  }

  /**
   * @private
   * @type {function(ol.layer.Layer): boolean}
   */
  this.layerFilter_ = layerFilter;

  /**
   * @private
   * @type {ol.FeatureOverlay}
   */
  this.featureOverlay_ = new ol.FeatureOverlay({
    style: goog.isDef(options.style) ? options.style :
        ol.interaction.Select.getDefaultStyleFunction()
  });

  var features = this.featureOverlay_.getFeatures();
  goog.events.listen(features, ol.CollectionEventType.ADD,
      this.addFeature_, false, this);
  goog.events.listen(features, ol.CollectionEventType.REMOVE,
      this.removeFeature_, false, this);

};
goog.inherits(ol.interaction.Select, ol.interaction.Interaction);


/**
 * Get the selected features.
 * @return {ol.Collection.<ol.Feature>} Features collection.
 * @api stable
 */
ol.interaction.Select.prototype.getFeatures = function() {
  return this.featureOverlay_.getFeatures();
};


/**
 * @param {ol.MapBrowserEvent} mapBrowserEvent Map browser event.
 * @return {boolean} `false` to stop event propagation.
 * @this {ol.interaction.Select}
 * @api
 */
ol.interaction.Select.handleEvent = function(mapBrowserEvent) {
  if (!this.condition_(mapBrowserEvent)) {
    return true;
  }
  var add = this.addCondition_(mapBrowserEvent);
  var remove = this.removeCondition_(mapBrowserEvent);
  var toggle = this.toggleCondition_(mapBrowserEvent);
  var set = !add && !remove && !toggle;
  var map = mapBrowserEvent.map;
  var features = this.featureOverlay_.getFeatures();
  var /** @type {Array.<ol.Feature>} */ deselected = [];
  var /** @type {Array.<ol.Feature>} */ selected = [];
  var change = false;
  if (set) {
    // Replace the currently selected feature(s) with the feature(s) at the
    // pixel, or clear the selected feature(s) if there is no feature at
    // the pixel.
    map.forEachFeatureAtPixel(mapBrowserEvent.pixel,
        /**
         * @param {ol.Feature} feature Feature.
         * @param {ol.layer.Layer} layer Layer.
         */
        function(feature, layer) {
          selected.push(feature);
        }, undefined, this.layerFilter_);
    if (selected.length > 0 && features.getLength() == 1 &&
        features.item(0) == selected[0]) {
      // No change
    } else {
      change = true;
      if (features.getLength() !== 0) {
        deselected = Array.prototype.concat(features.getArray());
        features.clear();
      }
      if (this.multi_) {
        features.extend(selected);
      } else if (selected.length > 0) {
        features.push(selected[0]);
      }
    }
  } else {
    // Modify the currently selected feature(s).
    map.forEachFeatureAtPixel(mapBrowserEvent.pixel,
        /**
         * @param {ol.Feature} feature Feature.
         * @param {ol.layer.Layer} layer Layer.
         */
        function(feature, layer) {
          var index = goog.array.indexOf(features.getArray(), feature);
          if (index == -1) {
            if (add || toggle) {
              selected.push(feature);
            }
          } else {
            if (remove || toggle) {
              deselected.push(feature);
            }
          }
        }, undefined, this.layerFilter_);
    var i;
    for (i = deselected.length - 1; i >= 0; --i) {
      features.remove(deselected[i]);
    }
    features.extend(selected);
    if (selected.length > 0 || deselected.length > 0) {
      change = true;
    }
  }
  if (change) {
    this.dispatchEvent(
        new ol.SelectEvent(ol.SelectEventType.SELECT, selected, deselected));
  }
  return ol.events.condition.pointerMove(mapBrowserEvent);
};


/**
 * Remove the interaction from its current map, if any,  and attach it to a new
 * map, if any. Pass `null` to just remove the interaction from the current map.
 * @param {ol.Map} map Map.
 * @api stable
 */
ol.interaction.Select.prototype.setMap = function(map) {
  var currentMap = this.getMap();
  var selectedFeatures = this.featureOverlay_.getFeatures();
  if (!goog.isNull(currentMap)) {
    selectedFeatures.forEach(currentMap.unskipFeature, currentMap);
  }
  goog.base(this, 'setMap', map);
  this.featureOverlay_.setMap(map);
  if (!goog.isNull(map)) {
    selectedFeatures.forEach(map.skipFeature, map);
  }
};


/**
 * @return {ol.style.StyleFunction} Styles.
 */
ol.interaction.Select.getDefaultStyleFunction = function() {
  var styles = ol.style.createDefaultEditingStyles();
  goog.array.extend(styles[ol.geom.GeometryType.POLYGON],
      styles[ol.geom.GeometryType.LINE_STRING]);
  goog.array.extend(styles[ol.geom.GeometryType.GEOMETRY_COLLECTION],
      styles[ol.geom.GeometryType.LINE_STRING]);

  return function(feature, resolution) {
    return styles[feature.getGeometry().getType()];
  };
};


/**
 * @param {ol.CollectionEvent} evt Event.
 * @private
 */
ol.interaction.Select.prototype.addFeature_ = function(evt) {
  var feature = evt.element;
  var map = this.getMap();
  goog.asserts.assertInstanceof(feature, ol.Feature);
  if (!goog.isNull(map)) {
    map.skipFeature(feature);
  }
};


/**
 * @param {ol.CollectionEvent} evt Event.
 * @private
 */
ol.interaction.Select.prototype.removeFeature_ = function(evt) {
  var feature = evt.element;
  var map = this.getMap();
  goog.asserts.assertInstanceof(feature, ol.Feature);
  if (!goog.isNull(map)) {
    map.unskipFeature(feature);
  }
};
