/*! For license information please see e68ca991.js.LICENSE.txt */
"use strict";(self.webpackChunksas_frontend=self.webpackChunksas_frontend||[]).push([[9075],{15112:(e,t,i)=>{i.d(t,{P:()=>n});i(94604);var r=i(9672);class n{constructor(e){n[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return n.types[e]&&n.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=n.types[t]=n.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=n.types[this.type];return e?Object.keys(e).map((function(e){return s[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}n[" "]=function(){},n.types={};var s=n.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var r=new n({type:e,key:t});return void 0!==i&&i!==r.value?r.value=i:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new n({type:this.type,key:e}).value}})},96305:(e,t,i)=>{i.d(t,{v:()=>r});const r=(e,t)=>e&&Object.keys(e.services).filter((i=>t in e.services[i]))},77980:(e,t,i)=>{i.r(t),i.d(t,{HaConfigServerControl:()=>w});i(53918),i(53268),i(12730),i(30879);var r=i(37500),n=i(26767),s=i(5701),o=i(17717),a=i(96305),l=i(7323),c=(i(54909),i(22098),i(41886)),d=i(5986),h=(i(1359),i(11654)),u=(i(88165),i(59695));function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var s="static"===n?e:i;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!m(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,s=n.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[s])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return b(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?b(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=k(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function f(e){var t,i=k(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function v(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function m(e){return e.decorators&&e.decorators.length}function y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function k(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}let w=function(e,t,i,r){var n=p();if(r)for(var s=0;s<r.length;s++)n=r[s](n);var o=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var n,s=e[r];if("method"===s.kind&&(n=t.find(i)))if(y(s.descriptor)||y(n.descriptor)){if(m(s)||m(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(m(s)){if(m(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}v(s,n)}else t.push(s)}return t}(o.d.map(f)),e);return n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([(0,n.M)("ha-config-server-control")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.C)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,s.C)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,s.C)()],key:"route",value:void 0},{kind:"field",decorators:[(0,s.C)()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,o.S)()],key:"_validating",value:()=>!1},{kind:"field",decorators:[(0,o.S)()],key:"_reloadableDomains",value:()=>[]},{kind:"field",key:"_validateLog",value:()=>""},{kind:"field",key:"_isValid",value:()=>null},{kind:"method",key:"updated",value:function(e){const t=e.get("hass");!e.has("hass")||t&&t.config.components===this.hass.config.components||(this._reloadableDomains=(0,a.v)(this.hass,"reload").sort())}},{kind:"method",key:"render",value:function(){return r.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        back-path="/config"
        .tabs=${u.configSections.general}
        .showAdvanced=${this.showAdvanced}
      >
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header"
            >${this.hass.localize("ui.panel.config.server_control.caption")}</span
          >
          <span slot="introduction"
            >${this.hass.localize("ui.panel.config.server_control.description")}</span
          >

          ${this.showAdvanced?r.dy` <ha-card
                header=${this.hass.localize("ui.panel.config.server_control.section.validation.heading")}
              >
                <div class="card-content">
                  ${this.hass.localize("ui.panel.config.server_control.section.validation.introduction")}
                  ${this._validateLog?r.dy`
                        <div class="config-invalid">
                          <span class="text">
                            ${this.hass.localize("ui.panel.config.server_control.section.validation.invalid")}
                          </span>
                          <mwc-button raised @click=${this._validateConfig}>
                            ${this.hass.localize("ui.panel.config.server_control.section.validation.check_config")}
                          </mwc-button>
                        </div>
                        <div id="configLog" class="validate-log">
                          ${this._validateLog}
                        </div>
                      `:r.dy`
                        <div
                          class="validate-container layout vertical center-center"
                        >
                          ${this._validating?r.dy`
                                <ha-circular-progress
                                  active
                                ></ha-circular-progress>
                              `:r.dy`
                                ${this._isValid?r.dy` <div
                                      class="validate-result"
                                      id="result"
                                    >
                                      ${this.hass.localize("ui.panel.config.server_control.section.validation.valid")}
                                    </div>`:""}
                                <mwc-button
                                  raised
                                  @click=${this._validateConfig}
                                >
                                  ${this.hass.localize("ui.panel.config.server_control.section.validation.check_config")}
                                </mwc-button>
                              `}
                        </div>
                      `}
                </div>
              </ha-card>`:""}

          <ha-card
            header=${this.hass.localize("ui.panel.config.server_control.section.server_management.heading")}
          >
            <div class="card-content">
              ${this.hass.localize("ui.panel.config.server_control.section.server_management.introduction")}
            </div>
            <div class="card-actions warning">
              <ha-call-service-button
                class="warning"
                .hass=${this.hass}
                domain="smartautomatic"
                service="restart"
                .confirmation=${this.hass.localize("ui.panel.config.server_control.section.server_management.confirm_restart")}
                >${this.hass.localize("ui.panel.config.server_control.section.server_management.restart")}
              </ha-call-service-button>
              ${(0,l.p)(this.hass,"saserver")?"":r.dy`<ha-call-service-button
                    class="warning"
                    .hass=${this.hass}
                    domain="smartautomatic"
                    service="stop"
                    confirmation=${this.hass.localize("ui.panel.config.server_control.section.server_management.confirm_stop")}
                    >${this.hass.localize("ui.panel.config.server_control.section.server_management.stop")}
                  </ha-call-service-button>`}
            </div>
          </ha-card>

          ${this.showAdvanced?r.dy`
                <ha-card
                  header=${this.hass.localize("ui.panel.config.server_control.section.reloading.heading")}
                >
                  <div class="card-content">
                    ${this.hass.localize("ui.panel.config.server_control.section.reloading.introduction")}
                  </div>
                  <div class="card-actions">
                    <ha-call-service-button
                      .hass=${this.hass}
                      domain="smartautomatic"
                      service="reload_core_config"
                      >${this.hass.localize("ui.panel.config.server_control.section.reloading.core")}
                    </ha-call-service-button>
                  </div>
                  ${this._reloadableDomains.map((e=>r.dy`<div class="card-actions">
                        <ha-call-service-button
                          .hass=${this.hass}
                          .domain=${e}
                          service="reload"
                          >${this.hass.localize(`ui.panel.config.server_control.section.reloading.${e}`)||this.hass.localize("ui.panel.config.server_control.section.reloading.reload","domain",(0,d.Lh)(this.hass.localize,e))}
                        </ha-call-service-button>
                      </div>`))}
                </ha-card>
              `:""}
        </ha-config-section>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_validateConfig",value:async function(){this._validating=!0,this._validateLog="",this._isValid=null;const e=await(0,c.Ij)(this.hass);this._validating=!1,this._isValid="valid"===e.result,e.errors&&(this._validateLog=e.errors)}},{kind:"get",static:!0,key:"styles",value:function(){return[h.Qx,r.iv`
        .validate-container {
          height: 140px;
        }

        .validate-result {
          color: var(--success-color);
          font-weight: 500;
          margin-bottom: 1em;
        }

        .config-invalid {
          margin: 1em 0;
        }

        .config-invalid .text {
          color: var(--error-color);
          font-weight: 500;
        }

        .config-invalid mwc-button {
          float: right;
        }

        .validate-log {
          white-space: pre-line;
          direction: ltr;
        }

        ha-config-section {
          padding-bottom: 24px;
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=e68ca991.js.map