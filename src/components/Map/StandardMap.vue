<template>
  <l-map
    :bounds="bounds"
    :center="center"
    :zoom="zoom"
    @click="$emit('mapClick', arguments[0].latlng)"
    @moveend="$emit('mapMoveEnd', arguments[0].target)"
  >
    <l-tile-layer
      :url="url"
      :attribution="attribution"
    />
    <ExtendedMarker
      v-for="marker in markers"
      :key="marker.id"
      v-bind="marker"
      @dragend="$emit('markerMoved', $event.target._latlng, marker)"
      :opacity="opacityFor(marker)"
    >
      <l-popup
        v-if="marker.popupcontent"
        :content="marker.popupcontent"
      />
    </ExtendedMarker>
  </l-map>
</template>

<script>
import {
  LMap,
  LTileLayer,
  LPopup,
} from 'vue2-leaflet'

import ExtendedMarker from './ExtendedMarker'

import L from 'leaflet'
import 'leaflet.awesome-markers/dist/leaflet.awesome-markers.js'

// fix default marker icon. Should hopefully get fixed in Leaflet 1.3
// https://github.com/Leaflet/Leaflet/issues/4968
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
})

const SELECTED_OPACITY = 1
const UNSELECTED_OPACITY = 0.5

export default {
  components: {
    LMap, LTileLayer, ExtendedMarker, LPopup,
  },
  props: {
    markers: {
      required: true,
      type: Array,
    },
    selectedMarkerIds: {
      type: Array,
      required: false,
      default: () => [],
    },
    showAttribution: {
      type: Boolean,
      default: true,
    },
    defaultCenter: {
      type: Object,
      default: null,
    },
    preventZoom: {
      type: Boolean,
      default: false,
    },
    forceCenter: {
      type: Object,
      default: null,
    },
    forceZoom: {
      type: Number,
      default: null,
    },
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    }
  },
  methods: {
    opacityFor (marker) {
      if (!this.hasSelectedMarkers) return SELECTED_OPACITY
      return this.selectedMarkerIds.includes(marker.id) ? SELECTED_OPACITY : UNSELECTED_OPACITY
    },
    getMarker (id) {
      return this.markers.find(marker => marker.id === id)
    },
  },
  computed: {
    hasSelectedMarkers () {
      return this.selectedMarkers && this.selectedMarkers.length > 0
    },
    selectedMarkers () {
      if (this.selectedMarkerIds.length > 0) {
        return this.selectedMarkerIds.map(this.getMarker).filter(existsFilter)
      }
    },
    hasMarkers () {
      return this.markers && this.markers.length > 0
    },
    hasOneMarker () {
      return this.markers && this.markers.length === 1
    },
    markersForBound () {
      if (this.hasSelectedMarkers) {
        return this.selectedMarkers
      }
      return this.markers
    },
    attribution () {
      if (this.showAttribution) {
        return '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      }
      return ''
    },
    bounds () {
      if (this.forceCenter && !Number.isNaN(this.forceCenter.lat)) return null
      if (!this.preventZoom && this.hasMarkers && !this.hasOneMarker) {
        return L.latLngBounds(this.markersForBound.map(m => m.latLng)).pad(0.2)
      }
    },
    center () {
      if (this.forceCenter && !Number.isNaN(this.forceCenter.lat)) return [this.forceCenter.lat, this.forceCenter.lng]
      if (!this.bounds) {
        if (this.hasOneMarker) {
          const { lat, lng } = this.markersForBound[0].latLng
          return [lat, lng]
        }
        if (this.defaultCenter) {
          return [this.defaultCenter.latitude, this.defaultCenter.longitude]
        }
        return ['49.8990022441358', '8.66415739059448']
      }
    },
    zoom () {
      if (this.forceZoom) {
        return this.forceZoom
      }
      if (!this.preventZoom && !this.bounds) {
        if (this.defaultCenter) {
          return 10
        }
        return 15
      }
    },
  },
}

function existsFilter (val) {
  return !!val
}
</script>

<style>
@import "~leaflet/dist/leaflet.css";
@import "~leaflet.awesome-markers/dist/leaflet.awesome-markers.css";
</style>
