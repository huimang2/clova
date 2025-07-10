function e(e,t,i,o){var n,a=arguments.length,s=a<3?t:null===o?o=Object.getOwnPropertyDescriptor(t,i):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)s=Reflect.decorate(e,t,i,o);else for(var r=e.length-1;r>=0;r--)(n=e[r])&&(s=(a<3?n(s):a>3?n(t,i,s):n(t,i))||s);return a>3&&s&&Object.defineProperty(t,i,s),s}const t=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),o=new Map;class n{constructor(e,t){if(this._$cssResult$=!0,t!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){let e=o.get(this.cssText);return t&&void 0===e&&(o.set(this.cssText,e=new CSSStyleSheet),e.replaceSync(this.cssText)),e}toString(){return this.cssText}}const a=(e,...t)=>{const o=1===e.length?e[0]:t.reduce(((t,i,o)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+e[o+1]),e[0]);return new n(o,i)},s=t?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const i of e.cssRules)t+=i.cssText;return(e=>new n("string"==typeof e?e:e+"",i))(t)})(e):e;var r;const l=window.trustedTypes,c=l?l.emptyScript:"",d=window.reactiveElementPolyfillSupport,h={toAttribute(e,t){switch(t){case Boolean:e=e?c:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let i=e;switch(t){case Boolean:i=null!==e;break;case Number:i=null===e?null:Number(e);break;case Object:case Array:try{i=JSON.parse(e)}catch(e){i=null}}return i}},p=(e,t)=>t!==e&&(t==t||e==e),u={attribute:!0,type:String,converter:h,reflect:!1,hasChanged:p};class v extends HTMLElement{constructor(){super(),this._$Et=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Ei=null,this.o()}static addInitializer(e){var t;null!==(t=this.l)&&void 0!==t||(this.l=[]),this.l.push(e)}static get observedAttributes(){this.finalize();const e=[];return this.elementProperties.forEach(((t,i)=>{const o=this._$Eh(i,t);void 0!==o&&(this._$Eu.set(o,i),e.push(o))})),e}static createProperty(e,t=u){if(t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),!t.noAccessor&&!this.prototype.hasOwnProperty(e)){const i="symbol"==typeof e?Symbol():"__"+e,o=this.getPropertyDescriptor(e,i,t);void 0!==o&&Object.defineProperty(this.prototype,e,o)}}static getPropertyDescriptor(e,t,i){return{get(){return this[t]},set(o){const n=this[e];this[t]=o,this.requestUpdate(e,n,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||u}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),this.elementProperties=new Map(e.elementProperties),this._$Eu=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const i of t)this.createProperty(i,e[i])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const i=new Set(e.flat(1/0).reverse());for(const e of i)t.unshift(s(e))}else void 0!==e&&t.push(s(e));return t}static _$Eh(e,t){const i=t.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof e?e.toLowerCase():void 0}o(){var e;this._$Ep=new Promise((e=>this.enableUpdating=e)),this._$AL=new Map,this._$Em(),this.requestUpdate(),null===(e=this.constructor.l)||void 0===e||e.forEach((e=>e(this)))}addController(e){var t,i;(null!==(t=this._$Eg)&&void 0!==t?t:this._$Eg=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&(null===(i=e.hostConnected)||void 0===i||i.call(e))}removeController(e){var t;null===(t=this._$Eg)||void 0===t||t.splice(this._$Eg.indexOf(e)>>>0,1)}_$Em(){this.constructor.elementProperties.forEach(((e,t)=>{this.hasOwnProperty(t)&&(this._$Et.set(t,this[t]),delete this[t])}))}createRenderRoot(){var e;const i=null!==(e=this.shadowRoot)&&void 0!==e?e:this.attachShadow(this.constructor.shadowRootOptions);return((e,i)=>{t?e.adoptedStyleSheets=i.map((e=>e instanceof CSSStyleSheet?e:e.styleSheet)):i.forEach((t=>{const i=document.createElement("style"),o=window.litNonce;void 0!==o&&i.setAttribute("nonce",o),i.textContent=t.cssText,e.appendChild(i)}))})(i,this.constructor.elementStyles),i}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(e=this._$Eg)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostConnected)||void 0===t?void 0:t.call(e)}))}enableUpdating(e){}disconnectedCallback(){var e;null===(e=this._$Eg)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostDisconnected)||void 0===t?void 0:t.call(e)}))}attributeChangedCallback(e,t,i){this._$AK(e,i)}_$ES(e,t,i=u){var o,n;const a=this.constructor._$Eh(e,i);if(void 0!==a&&!0===i.reflect){const s=(null!==(n=null===(o=i.converter)||void 0===o?void 0:o.toAttribute)&&void 0!==n?n:h.toAttribute)(t,i.type);this._$Ei=e,null==s?this.removeAttribute(a):this.setAttribute(a,s),this._$Ei=null}}_$AK(e,t){var i,o,n;const a=this.constructor,s=a._$Eu.get(e);if(void 0!==s&&this._$Ei!==s){const e=a.getPropertyOptions(s),r=e.converter,l=null!==(n=null!==(o=null===(i=r)||void 0===i?void 0:i.fromAttribute)&&void 0!==o?o:"function"==typeof r?r:null)&&void 0!==n?n:h.fromAttribute;this._$Ei=s,this[s]=l(t,e.type),this._$Ei=null}}requestUpdate(e,t,i){let o=!0;void 0!==e&&(((i=i||this.constructor.getPropertyOptions(e)).hasChanged||p)(this[e],t)?(this._$AL.has(e)||this._$AL.set(e,t),!0===i.reflect&&this._$Ei!==e&&(void 0===this._$E_&&(this._$E_=new Map),this._$E_.set(e,i))):o=!1),!this.isUpdatePending&&o&&(this._$Ep=this._$EC())}async _$EC(){this.isUpdatePending=!0;try{await this._$Ep}catch(e){Promise.reject(e)}const e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var e;if(!this.isUpdatePending)return;this.hasUpdated,this._$Et&&(this._$Et.forEach(((e,t)=>this[t]=e)),this._$Et=void 0);let t=!1;const i=this._$AL;try{t=this.shouldUpdate(i),t?(this.willUpdate(i),null===(e=this._$Eg)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostUpdate)||void 0===t?void 0:t.call(e)})),this.update(i)):this._$EU()}catch(e){throw t=!1,this._$EU(),e}t&&this._$AE(i)}willUpdate(e){}_$AE(e){var t;null===(t=this._$Eg)||void 0===t||t.forEach((e=>{var t;return null===(t=e.hostUpdated)||void 0===t?void 0:t.call(e)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$EU(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$Ep}shouldUpdate(e){return!0}update(e){void 0!==this._$E_&&(this._$E_.forEach(((e,t)=>this._$ES(t,this[t],e))),this._$E_=void 0),this._$EU()}updated(e){}firstUpdated(e){}}var _;v.finalized=!0,v.elementProperties=new Map,v.elementStyles=[],v.shadowRootOptions={mode:"open"},null==d||d({ReactiveElement:v}),(null!==(r=globalThis.reactiveElementVersions)&&void 0!==r?r:globalThis.reactiveElementVersions=[]).push("1.0.2");const m=globalThis.trustedTypes,f=m?m.createPolicy("lit-html",{createHTML:e=>e}):void 0,g=`lit$${(Math.random()+"").slice(9)}$`,y="?"+g,b=`<${y}>`,$=document,S=(e="")=>$.createComment(e),C=e=>null===e||"object"!=typeof e&&"function"!=typeof e,T=Array.isArray,w=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,A=/-->/g,x=/>/g,E=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,O=/'/g,G=/"/g,k=/^(?:script|style|textarea)$/i,R=(e=>(t,...i)=>({_$litType$:e,strings:t,values:i}))(1),D=Symbol.for("lit-noChange"),I=Symbol.for("lit-nothing"),H=new WeakMap,M=(e,t,i)=>{var o,n;const a=null!==(o=null==i?void 0:i.renderBefore)&&void 0!==o?o:t;let s=a._$litPart$;if(void 0===s){const e=null!==(n=null==i?void 0:i.renderBefore)&&void 0!==n?n:null;a._$litPart$=s=new V(t.insertBefore(S(),e),e,void 0,null!=i?i:{})}return s._$AI(e),s},L=$.createTreeWalker($,129,null,!1),P=(e,t)=>{const i=e.length-1,o=[];let n,a=2===t?"<svg>":"",s=w;for(let t=0;t<i;t++){const i=e[t];let r,l,c=-1,d=0;for(;d<i.length&&(s.lastIndex=d,l=s.exec(i),null!==l);)d=s.lastIndex,s===w?"!--"===l[1]?s=A:void 0!==l[1]?s=x:void 0!==l[2]?(k.test(l[2])&&(n=RegExp("</"+l[2],"g")),s=E):void 0!==l[3]&&(s=E):s===E?">"===l[0]?(s=null!=n?n:w,c=-1):void 0===l[1]?c=-2:(c=s.lastIndex-l[2].length,r=l[1],s=void 0===l[3]?E:'"'===l[3]?G:O):s===G||s===O?s=E:s===A||s===x?s=w:(s=E,n=void 0);const h=s===E&&e[t+1].startsWith("/>")?" ":"";a+=s===w?i+b:c>=0?(o.push(r),i.slice(0,c)+"$lit$"+i.slice(c)+g+h):i+g+(-2===c?(o.push(void 0),t):h)}const r=a+(e[i]||"<?>")+(2===t?"</svg>":"");return[void 0!==f?f.createHTML(r):r,o]};class N{constructor({strings:e,_$litType$:t},i){let o;this.parts=[];let n=0,a=0;const s=e.length-1,r=this.parts,[l,c]=P(e,t);if(this.el=N.createElement(l,i),L.currentNode=this.el.content,2===t){const e=this.el.content,t=e.firstChild;t.remove(),e.append(...t.childNodes)}for(;null!==(o=L.nextNode())&&r.length<s;){if(1===o.nodeType){if(o.hasAttributes()){const e=[];for(const t of o.getAttributeNames())if(t.endsWith("$lit$")||t.startsWith(g)){const i=c[a++];if(e.push(t),void 0!==i){const e=o.getAttribute(i.toLowerCase()+"$lit$").split(g),t=/([.?@])?(.*)/.exec(i);r.push({type:1,index:n,name:t[2],strings:e,ctor:"."===t[1]?j:"?"===t[1]?q:"@"===t[1]?W:z})}else r.push({type:6,index:n})}for(const t of e)o.removeAttribute(t)}if(k.test(o.tagName)){const e=o.textContent.split(g),t=e.length-1;if(t>0){o.textContent=m?m.emptyScript:"";for(let i=0;i<t;i++)o.append(e[i],S()),L.nextNode(),r.push({type:2,index:++n});o.append(e[t],S())}}}else if(8===o.nodeType)if(o.data===y)r.push({type:2,index:n});else{let e=-1;for(;-1!==(e=o.data.indexOf(g,e+1));)r.push({type:7,index:n}),e+=g.length-1}n++}}static createElement(e,t){const i=$.createElement("template");return i.innerHTML=e,i}}function U(e,t,i=e,o){var n,a,s,r;if(t===D)return t;let l=void 0!==o?null===(n=i._$Cl)||void 0===n?void 0:n[o]:i._$Cu;const c=C(t)?void 0:t._$litDirective$;return(null==l?void 0:l.constructor)!==c&&(null===(a=null==l?void 0:l._$AO)||void 0===a||a.call(l,!1),void 0===c?l=void 0:(l=new c(e),l._$AT(e,i,o)),void 0!==o?(null!==(s=(r=i)._$Cl)&&void 0!==s?s:r._$Cl=[])[o]=l:i._$Cu=l),void 0!==l&&(t=U(e,l._$AS(e,t.values),l,o)),t}class B{constructor(e,t){this.v=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}p(e){var t;const{el:{content:i},parts:o}=this._$AD,n=(null!==(t=null==e?void 0:e.creationScope)&&void 0!==t?t:$).importNode(i,!0);L.currentNode=n;let a=L.nextNode(),s=0,r=0,l=o[0];for(;void 0!==l;){if(s===l.index){let t;2===l.type?t=new V(a,a.nextSibling,this,e):1===l.type?t=new l.ctor(a,l.name,l.strings,this,e):6===l.type&&(t=new K(a,this,e)),this.v.push(t),l=o[++r]}s!==(null==l?void 0:l.index)&&(a=L.nextNode(),s++)}return n}m(e){let t=0;for(const i of this.v)void 0!==i&&(void 0!==i.strings?(i._$AI(e,i,t),t+=i.strings.length-2):i._$AI(e[t])),t++}}class V{constructor(e,t,i,o){var n;this.type=2,this._$AH=I,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=i,this.options=o,this._$Cg=null===(n=null==o?void 0:o.isConnected)||void 0===n||n}get _$AU(){var e,t;return null!==(t=null===(e=this._$AM)||void 0===e?void 0:e._$AU)&&void 0!==t?t:this._$Cg}get parentNode(){let e=this._$AA.parentNode;const t=this._$AM;return void 0!==t&&11===e.nodeType&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=U(this,e,t),C(e)?e===I||null==e||""===e?(this._$AH!==I&&this._$AR(),this._$AH=I):e!==this._$AH&&e!==D&&this.$(e):void 0!==e._$litType$?this.T(e):void 0!==e.nodeType?this.S(e):(e=>{var t;return T(e)||"function"==typeof(null===(t=e)||void 0===t?void 0:t[Symbol.iterator])})(e)?this.M(e):this.$(e)}A(e,t=this._$AB){return this._$AA.parentNode.insertBefore(e,t)}S(e){this._$AH!==e&&(this._$AR(),this._$AH=this.A(e))}$(e){this._$AH!==I&&C(this._$AH)?this._$AA.nextSibling.data=e:this.S($.createTextNode(e)),this._$AH=e}T(e){var t;const{values:i,_$litType$:o}=e,n="number"==typeof o?this._$AC(e):(void 0===o.el&&(o.el=N.createElement(o.h,this.options)),o);if((null===(t=this._$AH)||void 0===t?void 0:t._$AD)===n)this._$AH.m(i);else{const e=new B(n,this),t=e.p(this.options);e.m(i),this.S(t),this._$AH=e}}_$AC(e){let t=H.get(e.strings);return void 0===t&&H.set(e.strings,t=new N(e)),t}M(e){T(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let i,o=0;for(const n of e)o===t.length?t.push(i=new V(this.A(S()),this.A(S()),this,this.options)):i=t[o],i._$AI(n),o++;o<t.length&&(this._$AR(i&&i._$AB.nextSibling,o),t.length=o)}_$AR(e=this._$AA.nextSibling,t){var i;for(null===(i=this._$AP)||void 0===i||i.call(this,!1,!0,t);e&&e!==this._$AB;){const t=e.nextSibling;e.remove(),e=t}}setConnected(e){var t;void 0===this._$AM&&(this._$Cg=e,null===(t=this._$AP)||void 0===t||t.call(this,e))}}class z{constructor(e,t,i,o,n){this.type=1,this._$AH=I,this._$AN=void 0,this.element=e,this.name=t,this._$AM=o,this.options=n,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=I}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(e,t=this,i,o){const n=this.strings;let a=!1;if(void 0===n)e=U(this,e,t,0),a=!C(e)||e!==this._$AH&&e!==D,a&&(this._$AH=e);else{const o=e;let s,r;for(e=n[0],s=0;s<n.length-1;s++)r=U(this,o[i+s],t,s),r===D&&(r=this._$AH[s]),a||(a=!C(r)||r!==this._$AH[s]),r===I?e=I:e!==I&&(e+=(null!=r?r:"")+n[s+1]),this._$AH[s]=r}a&&!o&&this.k(e)}k(e){e===I?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class j extends z{constructor(){super(...arguments),this.type=3}k(e){this.element[this.name]=e===I?void 0:e}}const F=m?m.emptyScript:"";class q extends z{constructor(){super(...arguments),this.type=4}k(e){e&&e!==I?this.element.setAttribute(this.name,F):this.element.removeAttribute(this.name)}}class W extends z{constructor(e,t,i,o,n){super(e,t,i,o,n),this.type=5}_$AI(e,t=this){var i;if((e=null!==(i=U(this,e,t,0))&&void 0!==i?i:I)===D)return;const o=this._$AH,n=e===I&&o!==I||e.capture!==o.capture||e.once!==o.once||e.passive!==o.passive,a=e!==I&&(o===I||n);n&&this.element.removeEventListener(this.name,this,o),a&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){var t,i;"function"==typeof this._$AH?this._$AH.call(null!==(i=null===(t=this.options)||void 0===t?void 0:t.host)&&void 0!==i?i:this.element,e):this._$AH.handleEvent(e)}}class K{constructor(e,t,i){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(e){U(this,e)}}const Z=window.litHtmlPolyfillSupport;var J,Q;null==Z||Z(N,V),(null!==(_=globalThis.litHtmlVersions)&&void 0!==_?_:globalThis.litHtmlVersions=[]).push("2.0.2");class Y extends v{constructor(){super(...arguments),this.renderOptions={host:this},this._$Dt=void 0}createRenderRoot(){var e,t;const i=super.createRenderRoot();return null!==(e=(t=this.renderOptions).renderBefore)&&void 0!==e||(t.renderBefore=i.firstChild),i}update(e){const t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Dt=M(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null===(e=this._$Dt)||void 0===e||e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this._$Dt)||void 0===e||e.setConnected(!1)}render(){return D}}Y.finalized=!0,Y._$litElement$=!0,null===(J=globalThis.litElementHydrateSupport)||void 0===J||J.call(globalThis,{LitElement:Y});const X=globalThis.litElementPolyfillSupport;null==X||X({LitElement:Y}),(null!==(Q=globalThis.litElementVersions)&&void 0!==Q?Q:globalThis.litElementVersions=[]).push("3.0.2");const ee=e=>t=>"function"==typeof t?((e,t)=>(window.customElements.define(e,t),t))(e,t):((e,t)=>{const{kind:i,elements:o}=t;return{kind:i,elements:o,finisher(t){window.customElements.define(e,t)}}})(e,t),te=(e,t)=>"method"===t.kind&&t.descriptor&&!("value"in t.descriptor)?{...t,finisher(i){i.createProperty(t.key,e)}}:{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:t.key,initializer(){"function"==typeof t.initializer&&(this[t.key]=t.initializer.call(this))},finisher(i){i.createProperty(t.key,e)}};function ie(e){return(t,i)=>void 0!==i?((e,t,i)=>{t.constructor.createProperty(i,e)})(e,t,i):te(e,t)}function oe(e){return ie({...e,state:!0})}const ne=({finisher:e,descriptor:t})=>(i,o)=>{var n;if(void 0===o){const o=null!==(n=i.originalKey)&&void 0!==n?n:i.key,a=null!=t?{kind:"method",placement:"prototype",key:o,descriptor:t(i.key)}:{...i,key:o};return null!=e&&(a.finisher=function(t){e(t,o)}),a}{const n=i.constructor;void 0!==t&&Object.defineProperty(i,o,t(o)),null==e||e(n,o)}};function ae(){return document.querySelector("hc-main")?document.querySelector("hc-main").hass:document.querySelector("home-assistant")?document.querySelector("home-assistant").hass:void 0}function se(){var e,t,i,o;return(null===(o=null===(i=null===(t=null===(e=document.querySelector("home-assistant"))||void 0===e?void 0:e.shadowRoot)||void 0===t?void 0:t.querySelector("home-assistant-main"))||void 0===i?void 0:i.shadowRoot)||void 0===o?void 0:o.querySelector("clova-panel"))||void 0}function re(e){return ae().localize(`component.clova.${e}`)}async function le(e,t,i=!1){let o=e;"string"==typeof t&&(t=t.split(/(\$| )/)),""===t[t.length-1]&&t.pop();for(const[e,n]of t.entries())if(n.trim().length){if(!o)return null;o.localName&&o.localName.includes("-")&&await customElements.whenDefined(o.localName),o.updateComplete&&await o.updateComplete,o="$"===n?i&&e==t.length-1?[o.shadowRoot]:o.shadowRoot:i&&e==t.length-1?o.querySelectorAll(n):o.querySelector(n)}return o}async function ce(e,t,i=!1){const o=document.querySelector("home-assistant");if(!o)return;let n=await async function(e,t,i=!1,o=1e4){return Promise.race([le(e,t,i),new Promise(((e,t)=>setTimeout((()=>t(new Error("timeout"))),o)))]).catch((e=>{if(!e.message||"timeout"!==e.message)throw e;return null}))}(o,"$ clova-popup");if(!n){n=document.createElement("clova-popup");const e=o.shadowRoot.querySelector("ha-more-info-dialog");e?o.shadowRoot.insertBefore(n,e):o.shadowRoot.appendChild(n)}history.replaceState({ClovaPopup:!1},""),history.pushState({ClovaPopup:!0,params:{title:e,card:t,large:i}},""),n.showDialog(e,t,i)}const de=async()=>{if(customElements.get("developer-tools-event"))return;await customElements.whenDefined("partial-panel-resolver");const e=document.createElement("partial-panel-resolver");e.hass={panels:[{url_path:"tmp",component_name:"developer-tools"}]},e._updateRoutes(),await e.routerOptions.routes.tmp.load(),await customElements.whenDefined("developer-tools-router")};console.warn("The main 'lit-element' module entrypoint is deprecated. Please update your imports to use the 'lit' package: 'lit' and 'lit/decorators.ts' or import from 'lit-element/lit-element.ts'. See https://lit.dev/msg/deprecated-import-path for more information.");const he=(e,t,i,o)=>{o=o||{},i=null==i?{}:i;const n=new Event(t,{bubbles:void 0===o.bubbles||o.bubbles,cancelable:Boolean(o.cancelable),composed:void 0===o.composed||o.composed});return n.detail=i,e.dispatchEvent(n),n},pe=t=>{class i extends t{connectedCallback(){super.connectedCallback(),(se()||this).addEventListener("clova-updated",this._event_listenser=e=>this._updated(e))}disconnectedCallback(){se()&&(se().removeEventListener("clova-updated",this._event_listenser),this._event_listenser=void 0),super.disconnectedCallback()}async _updated(e){({connect:e=>this._connect(e),update:e=>this._update(e)})[e.detail.command](e.detail)}_connect(e){throw new Error("Method not implemented.")}_update(e){throw new Error("Method not implemented.")}}return e([oe()],i.prototype,"_event_listenser",void 0),i},ue=t=>{class i extends t{connectedCallback(){super.connectedCallback(),this.hass=se().hass}}return e([ie({type:Object})],i.prototype,"hass",void 0),i},ve=t=>{class i extends t{connectedCallback(){super.connectedCallback(),this.connect()}disconnectedCallback(){super.disconnectedCallback(),this._ws_connection.commands.get(this._ws_id).unsubscribe()}async connect(){if(null!==document.querySelector("hc-main"))this._ws_connection=ae().connection;else{if(!window.hassConnection)return void window.setTimeout((()=>this.connect()),100);this._ws_connection=(await window.hassConnection).conn}this._ws_connection.subscribeMessage((e=>he(this,"clova-updated",e)),{type:"clova/connect"})}}return e([ie()],i.prototype,"_ws_connection",void 0),e([oe()],i.prototype,"_ws_id",void 0),i},_e=e=>class extends e{constructor(){super(...arguments),this._ClovaPopupListener=e=>{var t,i;if(null===(t=e.state)||void 0===t?void 0:t.ClovaPopup){const{title:t,card:i,large:o}=e.state.params;this.showDialog(t,i,o)}else!1===(null===(i=e.state)||void 0===i?void 0:i.ClovaPopup)&&this.closePopup()}}connectedCallback(){super.connectedCallback(),window.addEventListener("popstate",this._ClovaPopupListener)}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("popstate",this._ClovaPopupListener)}closePopup(){throw new Error("Method not implemented.")}showDialog(e,t,i){throw new Error("Method not implemented.")}},me="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",fe={AIRCONDITIONER:["ChangeFanSpeed","ChangeMode","ChangePower","DecrementFanSpeed","DecrementTargetTemperature","GetCurrentTemperature","GetDeviceState","GetTargetTemperature","HealthCheck","IncrementFanSpeed","IncrementTargetTemperature","SetFanSpeed","SetMode","SetTargetTemperature","StartOscillation","StopOscillation","TurnOff","TurnOn"],AIRPURIFIER:["ChangeFanSpeed","ChangeMode","ChangePower","DecrementFanSpeed","GetAirQuality","GetCurrentTemperature","GetDeviceState","GetFineDust","GetHumidity","GetUltraFineDust","HealthCheck","IncrementFanSpeed","ReleaseMode","SetFanSpeed","SetMode","TurnOff","TurnOn"],AIRSENSOR:["GetAirQuality","GetCurrentTemperature","GetDeviceState","GetFineDust","GetHumidity","GetUltraFineDust","HealthCheck"],BIDET:["Close","GetDeviceState","GetExpendableState","HealthCheck","Open","TurnOff","TurnOn"],BODYWEIGHTSCALE:["GetBMI","GetBatteryInfo","GetDeviceState","GetBodyFat","GetHealthScore","GetMuscle","GetWeight","HealthCheck"],BUILDING_ELECTRIC_METER:["GetConsumption"],BUILDING_ELEVATOR_CALLER:["CallElevator"],BUILDING_GAS_METER:["GetConsumption"],BUILDING_HEATING_METER:["GetConsumption"],BUILDING_HOTWATER_METER:["GetConsumption"],BUILDING_NOTICE_MONITOR:["GetNotice"],BUILDING_PACKAGE:["GetPackage"],BUILDING_PARKING_MONITOR:["GetVehicleLocation"],BUILDING_UTILITY_BILL_MONITOR:["GetCurrentBill"],BUILDING_WATER_METER:["GetConsumption"],CLOTHESCAREMACHINE:["GetDeviceState","GetPhase","GetRemainingTime","HealthCheck","TurnOff","TurnOn"],CLOTHESDRYER:["GetDeviceState","GetPhase","GetRemainingTime","HealthCheck","TurnOff","TurnOn"],CLOTHESWASHER:["GetDeviceState","GetPhase","GetRemainingTime","HealthCheck","TurnOff","TurnOn"],DEHUMIDIFIER:["GetCurrentTemperature","GetDeviceState","GetHumidity","HealthCheck","SetFanSpeed","TurnOff","TurnOn"],DISHWASHER:["GetDeviceState","GetPhase","GetRemainingTime","HealthCheck","TurnOff","TurnOn"],ELECTRICKETTLE:["GetCurrentTemperature","GetDeviceState","HealthCheck","TurnOff","TurnOn"],ELECTRICTOOTHBRUSH:["GetDeviceState","HealthCheck"],FAN:["DecrementFanSpeed","GetDeviceState","HealthCheck","IncrementFanSpeed","SetFanSpeed","SetMode","StartOscillation","StopOscillation","TurnOff","TurnOn"],HEATER:["DecrementTargetTemperature","GetCurrentTemperature","GetDeviceState","GetTargetTemperature","HealthCheck","IncrementTargetTemperature","SetTargetTemperature","TurnOff","TurnOn"],HOMECAM:["GetDetectionCount","HealthCheck","ReleaseMode","SetMode","StartRecording","StopRecording","TurnOff","TurnOn"],HUMIDIFIER:["GetCurrentTemperature","GetDeviceState","GetHumidity","HealthCheck","ReleaseMode","SetFanSpeed","SetMode","TurnOff","TurnOn"],KIMCHIREFRIGERATOR:["GetDeviceState","HealthCheck"],LIGHT:["DecrementBrightness","DecrementVolume HealthCheck","GetDeviceState","IncrementBrightness","IncrementVolume","ReleaseMode","SetBrightness","SetColor","SetColorTemperature","SetMode","TurnOff","TurnOn"],MASSAGECHAIR:["DecrementIntensityLevel","GetDeviceState","HealthCheck","IncrementIntensityLevel","TurnOff","TurnOn"],MICROWAVE:["GetDeviceState","GetRemainingTime","HealthCheck","TurnOff","TurnOn"],MOTIONSENSOR:["GetDetectedTime","GetDeviceState","GetPowerState","HealthCheck","ReleaseMode","SetMode","TurnOff","TurnOn"],OPENCLOSESENSOR:["GetCloseTime","GetDeviceState","GetOpenState","GetOpenTime","HealthCheck"],OVEN:["GetDeviceState","GetRemainingTime","HealthCheck","Preheat"],POWERSTRIP:["GetConsumption","GetDeviceState","GetEstimateBill","GetProgressiveTaxBracket","HealthCheck","TurnOff","TurnOn"],PURIFIER:["GetConsumption","GetDeviceState","GetExpendableState","HealthCheck","ReleaseMode","SetMode","SetTargetTemperature"],RANGE:["GetDeviceState","HealthCheck"],RANGEHOOD:["GetDeviceState","HealthCheck","TurnOff","TurnOn"],REFRIGERATOR:["GetDeviceState","HealthCheck","ReleaseMode","SetMode","SetTargetTemperature"],RICECOOKER:["GetCleaningCycle","GetDeviceState","GetExpendableState","GetKeepWarmTime","GetPhase","GetRemainingTime","HealthCheck","ReleaseMode","SetMode","Stop","TurnOff","TurnOn"],ROBOTVACUUM:["Charge","GetBatteryInfo","GetDeviceState","HealthCheck","TurnOff","TurnOn"],SETTOPBOX:["ChangeInputSource","ChangePower","DecrementChannel","DecrementVolume","GetDeviceState","HealthCheck","IncrementChannel","IncrementVolume","Mute","SetChannel","SetChannelByName","TurnOff","TurnOn","Unmute"],SLEEPINGMONITOR:["GetAsleepDuration","GetAwakeDuration","GetDeviceState","GetSleepScore","GetSleepStartTime","HealthCheck","TurnOff","TurnOn"],SMARTBED:["GetDeviceState","HealthCheck","Lower","Raise","Stop"],SMARTCHAIR:["GetCurrentSittingState","GetDeviceState","GetRightPostureRatio","GetUsageTime","HealthCheck"],SMARTCURTAIN:["Close","GetDeviceState","HealthCheck","Open","Stop"],SMARTHUB:["GetCurrentTemperature","GetDeviceState","GetHumidity","GetTargetTemperature","HealthCheck","SetMode"],SMARTLOCK:["GetDeviceState","GetLockState","HealthCheck","SetLockState"],SMARTMETER:["GetConsumption","GetCurrentBill","GetDeviceState","GetEstimateBill","GetProgressiveTaxBracket","HealthCheck"],SMARTPLUG:["GetConsumption","GetDeviceState","GetEstimateBill","HealthCheck","TurnOff","TurnOn"],SMARTTV:["ChangeInputSource","ChangePower","DecrementChannel","DecrementVolume","GetDeviceState","HealthCheck","IncrementChannel","IncrementVolume","Mute","SetChannel","SetChannelByName","TurnOff","TurnOn","Unmute"],SMARTVALVE:["GetDeviceState","GetLockState","SetLockState"],SMOKESENSOR:["GetDeviceState","HealthCheck"],SWITCH:["GetDeviceState","HealthCheck","TurnOff","TurnOn"],THERMOSTAT:["DecrementTargetTemperature","GetConsumption","GetCurrentTemperature","GetDeviceState","GetEstimateConsumption","GetTargetTemperature","HealthCheck","IncrementTargetTemperature","SetMode","SetTargetTemperature TurnOff","TurnOn"],VENTILATOR:["GetAirQuality","GetCurrentTemperature","GetDeviceState","GetHumidity","GetTargetTemperature","HealthCheck","ReleaseMode","SetFanSpeed","SetMode","TurnOff","TurnOn"],WATERBOILER:["GetDeviceState","HealthCheck","SetMode","TurnOff","TurnOn"],WINECELLAR:["GetDeviceState","HealthCheck","ReleaseMode","SetMode","SetTargetTemperature","TurnOff","TurnOn"]},ge=Object.keys(fe),ye=e=>(null==fe?void 0:fe[e])||[],be=6;const $e={};const Se=(e=>(...t)=>({_$litDirective$:e,values:t}))(class extends class extends class{constructor(e){}get _$AU(){return this._$AM._$AU}_$AT(e,t,i){this._$Ct=e,this._$AM=t,this._$Ci=i}_$AS(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}}{constructor(e){if(super(e),this.previousValue=$e,e.type!==be)throw new Error("renderer only supports binding to element")}render(e,t){return I}update(e,[t,i]){var o;const n=this.previousValue===$e;if(!this.hasChanged(i))return I;this.previousValue=Array.isArray(i)?Array.from(i):i;const a=e.element;if(n){const i=null===(o=e.options)||void 0===o?void 0:o.host;this.addRenderer(a,t,{host:i})}else this.runRenderer(a);return I}hasChanged(e){let t=!0;return Array.isArray(e)?Array.isArray(this.previousValue)&&this.previousValue.length===e.length&&e.every(((e,t)=>e===this.previousValue[t]))&&(t=!1):this.previousValue===e&&(t=!1),t}}{addRenderer(e,t,i){e.renderer=(e,o,n)=>{M(t.call(i.host,n.item,n,o),e,i)}}runRenderer(e){e.requestContentUpdate()}});window.JSCompiler_renameProperty=function(e,t){return e};let Ce=[],Te=document.createTextNode("");new window.MutationObserver((function(){const e=Ce.length;for(let t=0;t<e;t++){let e=Ce[t];if(e)try{e()}catch(e){setTimeout((()=>{throw e}))}}Ce.splice(0,e)})).observe(Te,{characterData:!0});var we=Number.isNaN||function(e){return"number"==typeof e&&e!=e};function Ae(e,t){if(e.length!==t.length)return!1;for(var i=0;i<e.length;i++)if(o=e[i],n=t[i],!(o===n||we(o)&&we(n)))return!1;var o,n;return!0}let xe=class extends(ue(Y)){constructor(){super(...arguments),this.secondary=!0,this.rowRenderer=e=>R`
      <style>
        paper-item {
          padding: 0;
          margin: -10px;
          margin-left: 0px;
        }
        #content {
          display: flex;
          align-items: center;
        }
        :host([selected]) paper-item {
          margin-left: 10px;
        }
        ha-svg-icon {
          padding-left: 2px;
          margin-right: -2px;
          color: var(--secondary-text-color);
        }
        :host(:not([selected])) ha-svg-icon {
          display: none;
        }
        :host([selected]) paper-icon-item {
          margin-left: 0;
        }
      </style>
      <ha-svg-icon .path=${"M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"}></ha-svg-icon>
      <paper-item>
        <paper-item-body two-line>
          ${e.label}
          ${this.secondary?R`
            <span secondary>
              ${e.label.toLowerCase()===e.value.toLowerCase()?"":e.value.toLowerCase()}
            </span>
          `:""}
        </paper-item-body>
      </paper-item>
    `,this._filteredTypes=function(e,t){void 0===t&&(t=Ae);var i=null;function o(){for(var o=[],n=0;n<arguments.length;n++)o[n]=arguments[n];if(i&&i.lastThis===this&&t(o,i.lastArgs))return i.lastResult;var a=e.apply(this,o);return i={lastResult:a,lastArgs:o,lastThis:this},a}return o.clear=function(){i=null},o}(((e,t)=>{if(!e)return[];const i=e.reduce(((e,t)=>(e.push({value:t,label:re(`${this.prefix}.${t}`)}),e)),[]);return t?i.filter((e=>{var i;return e.value.toLowerCase().includes(t)||(null===(i=e.label)||void 0===i?void 0:i.toLowerCase().includes(t))})):i}))}focus(){this.updateComplete.then((()=>{var e,t;null===(t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("paper-input"))||void 0===t||t.focus()}))}get selectedItem(){return this._comboBox.selectedItem}open(){this.updateComplete.then((()=>{var e;null===(e=this._comboBox)||void 0===e||e.open()}))}_filterChanged(e){this._filter=e.detail.value.toLowerCase(),he(this,e.type,e.detail,{composed:!1})}_valueChanged(e){e.stopPropagation();e.detail.value!==this.value&&this.value&&(this.value=e.detail.value,he(this,"change"),he(this,"value-changed",{value:this.value}))}_clearValue(e){e.stopPropagation(),this.value=void 0}_openedChanged(e){this._opened=e.detail.value,he(this,e.type,e.detail)}render(){return R`
        <vaadin-combo-box-light
          .value=${this.value}
          .filteredItems=${this._filteredTypes(this.filteredItems,this._filter)}
          ${e=this.rowRenderer,Se(e,t)}
          item-value-path="value"
          item-label-path="label"
          @opened-changed=${this._openedChanged}
          @filter-changed=${this._filterChanged}
          @value-changed=${this._valueChanged}
			  >
          <paper-input
            .label=${this.label}
            .disabled=${this.disabled}
            class="input"
            autocapitalize="none"
            autocomplete="off"
            autocorrect="off"
            spellcheck="false"
          >
            ${this.value?R`
                  <ha-icon-button
                    .label=${this.hass.localize("ui.components.combo-box.clear")}
                    .path=${me}
                    slot="suffix"
                    class="clear-button"
                    @click=${this._clearValue}
                  ></ha-icon-button>
                `:""}

            <ha-icon-button
              .label=${this.hass.localize("ui.components.combo-box.show")}
              .path=${this._opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}
              slot="suffix"
              class="toggle-button"
            ></ha-icon-button>
            <span slot="helper">Helper text</span>
          </paper-input>
        </vaadin-combo-box-light>
      `;var e,t}static get styles(){return a`
        paper-input > ha-icon-button {
          --mdc-icon-button-size: 24px;
          padding: 2px;
          color: var(--secondary-text-color);
        }
      `}};e([ie({type:Object})],xe.prototype,"hass",void 0),e([ie({type:String})],xe.prototype,"label",void 0),e([ie({type:Array})],xe.prototype,"filteredItems",void 0),e([ie({type:String})],xe.prototype,"prefix",void 0),e([ie({type:String})],xe.prototype,"value",void 0),e([ie({type:Boolean})],xe.prototype,"secondary",void 0),e([ie({type:Boolean})],xe.prototype,"disabled",void 0),e([oe()],xe.prototype,"_opened",void 0),e([ie()],xe.prototype,"rowRenderer",void 0),e([function(e,t){return ne({descriptor:i=>{const o={get(){var t,i;return null!==(i=null===(t=this.renderRoot)||void 0===t?void 0:t.querySelector(e))&&void 0!==i?i:null},enumerable:!0,configurable:!0};if(t){const t="symbol"==typeof i?Symbol():"__"+i;o.get=function(){var i,o;return void 0===this[t]&&(this[t]=null!==(o=null===(i=this.renderRoot)||void 0===i?void 0:i.querySelector(e))&&void 0!==o?o:null),this[t]}}return o}})}("vaadin-combo-box-light",!0)],xe.prototype,"_comboBox",void 0),e([oe()],xe.prototype,"_filter",void 0),xe=e([ee("clova-combo-box")],xe);let Ee=class extends(ue(pe(Y))){_update(e){var t,i,o,n;this.config={entity_config:(null===(i=null===(t=e.data.clova_config)||void 0===t?void 0:t.entity_config)||void 0===i?void 0:i[this.entity_id])||{},default_config:this.config.default_config||{}},this.type=((null===(o=this.config.entity_config)||void 0===o?void 0:o.type)||(null===(n=this.config.default_config)||void 0===n?void 0:n.type)||"").toUpperCase()}render(){var e,t;return R`
			<paper-input
				always-float-label
				.value=${(null===(t=null===(e=this.config.entity_config)||void 0===e?void 0:e.name)||void 0===t?void 0:t.toString())||""}
				.label=${re("panel.label.name")}
				.key=${"name"}
				@blur=${this._valueChanged}
				.placeholder=${this.hass.states[this.entity_id].attributes.friendly_name}
			></paper-input>
			<paper-input
				.value=${this.entity_id}
				.label=${re("panel.label.entity_id")}
				.error-message=${re("panel.errorMessage.entity_id")}
				.disabled=${!0}
			></paper-input>
			<clova-combo-box
				.label=${re("panel.label.type")}
				.value=${this.type}
				.filteredItems=${ge}
        .prefix=${"type"}
        @value-changed=${this._typeChanged}
			></clova-combo-box>
			${["model","version","description"].reduce(((e,t)=>(e.push([re(`panel.label.${t}`),t]),e)),[]).map((([e,t])=>{var i,o;return R`
				<paper-input
					.label=${e}
					always-float-label
					.key=${t}
					.value=${(null===(i=this.config.entity_config)||void 0===i?void 0:i[t])||(null===(o=this.config.default_config)||void 0===o?void 0:o[t])||""}
					@blur=${this._valueChanged}
				></paper-input>
			`}))}
			<div class="row">
				<div>
					<div>${re("panel.label.expose")}</div>
					<div class="secondary">${re("panel.description.expose")}</div>
				</div>
				<ha-switch
					.checked=${this.config.entity_config.hasOwnProperty("expose")?this.config.entity_config.expose:this.expose_by_default}
					.key=${"expose"}
					@change=${this._valueChanged}
				></ha-switch>
			</div>
			<div class="row">
				<div>
					<div>${re("panel.label.ir")}</div>
					<div class="secondary">${re("panel.description.ir")}</div>
				</div>
				<ha-switch
					.checked=${!!this.config.entity_config.hasOwnProperty("ir")&&this.config.entity_config.ir}
					.key=${"ir"}
					@change=${this._valueChanged}
				></ha-switch>
			</div>
		`}static get styles(){return a`
			:host {
				--primary-text-color: #212121;
			}
			paper-dropdown-menu-light {
				width: 100%;
			}
			.row {
				margin: 8px 0;
				color: var(--primary-text-color);
				display: flex;
				align-items: center;
				justify-content: space-between;
			}
			ha-switch {
				min-width: 38px;
				margin: -4px -16px -4px 0;
				padding: 4px 16px;
			}
		`}async _valueChanged(e){var t,i;const o=e.target,n="paper-listbox"==o.localName.toLowerCase()?o.selectedItem.value:"ha-switch"==o.localName.toLowerCase()?o.checked:o.value;(null===(i=null===(t=this.config)||void 0===t?void 0:t.entity_config)||void 0===i?void 0:i[o.key])!=n&&se()._ws_connection.sendMessage({type:"clova/update",entity_id:this.entity_id,key:o.key,value:n})}async _typeChanged(e){var t,i;ge.includes(e.detail.value)&&(this.type=e.detail.value),(null===(i=null===(t=this.config)||void 0===t?void 0:t.entity_config)||void 0===i?void 0:i.type)!=this.type&&se()._ws_connection.sendMessage({type:"clova/update",entity_id:this.entity_id,key:"type",value:this.type})}};e([ie({type:Object})],Ee.prototype,"hass",void 0),e([ie({type:String})],Ee.prototype,"entity_id",void 0),e([ie({type:Object})],Ee.prototype,"config",void 0),e([ie({type:Boolean})],Ee.prototype,"expose_by_default",void 0),e([ie({type:String})],Ee.prototype,"type",void 0),Ee=e([ee("clova-info-basic")],Ee);let Oe=class extends(ue(pe(Y))){constructor(){super(...arguments),this._curIndex=0,this._customActions=[],this._remainActions=[],this._actionDetail={},this._action="",this._service="",this._serviceData={},this._responseData={}}render(){var e,t,i,o,n,a,s;return this._customActions=Object.keys((null===(e=this.config.entity_config)||void 0===e?void 0:e.actionDetails)||{}).filter((e=>ye(this.type).includes(e)))||[],this._action=this._customActions[this._curIndex]||"",this._remainActions=ye(this.type).filter((e=>!this._customActions.includes(e)||e===this._action))||[],this._actionDetail=(null===(i=Object.values((null===(t=this.config.entity_config)||void 0===t?void 0:t.actionDetails)||{}))||void 0===i?void 0:i[this._curIndex])||{},this._service=(null===(o=this._actionDetail)||void 0===o?void 0:o.service)||"",this._serviceData=this._action&&this._service?{service:(null===(n=this._actionDetail)||void 0===n?void 0:n.service)||"",data:(null===(a=this._actionDetail)||void 0===a?void 0:a.data)||{}}:{},this._responseData=(null===(s=this._actionDetail)||void 0===s?void 0:s.response)||{},R`
			<div class="card-config">
				<div class="toolbar">
					<paper-tabs
						.selected=${this._curIndex}
						scrollable
						@iron-activate=${this._handleSelectedCard}
					>
						${this._customActions.map(((e,t)=>R`<paper-tab>${t+1}</paper-tab>`))}
					</paper-tabs>
					<paper-tabs
						id="add-card"
						.selected=${this._curIndex===this._customActions.length?"0":void 0}
						@iron-activate=${this._handleSelectedCard}
					>
						<paper-tab>
							<ha-svg-icon .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
						</paper-tab>
					</paper-tabs>
				</div>
				<div class="content">
          <clova-combo-box
            .label=${re("panel.label.action")}
            .value=${this._action}
            .filteredItems=${this._remainActions}
            .prefix=${"action"}
					></clova-combo-box>
					</paper-dropdown-menu-light>
					<ha-yaml-editor
						.defaultValue=${this._responseData}
						@value-changed=${this._dataChanged}
					></ha-yaml-editor>
					<ha-service-picker
						.hass=${this.hass}
						.value=${this._service}
						@value-changed=${this._serviceChanged}
					></ha-service-picker>
					<ha-yaml-editor
						.defaultValue=${this._serviceData}
					></ha-yaml-editor>
				</div>
			</div>
		`}static get styles(){return a`
			.toolbar {
				display: flex;
				--paper-tabs-selection-bar-color: var(--primary-color);
				--paper-tab-ink: var(--primary-color);
			}
			paper-dropdown-menu-light {
				width: 100%;
			}
			paper-tabs {
				--paper-tabs-selection-bar-color: var(--primary-color);
				color: var(--primary-text-color);
				text-transform: uppercase;
				border-bottom: 1px solid rgba(0, 0, 0, 0.1);
				padding: 0 20px;
				display: flex;
				font-size: 14px;
				flex-grow: 1;
			}
			paper-tabs {
				display: flex;
				font-size: 14px;
				flex-grow: 1;
			}
			#add-card {
				max-width: 32px;
				padding: 0px;
			}
		`}_handleSelectedCard(e){"add-card"!==e.target.id?this._curIndex=parseInt(e.detail.selected,10):this._curIndex=this._customActions.length}_dataChanged(e){e.stopPropagation(),e.detail.isValid}_serviceChanged(e){e.stopPropagation(),e.detail.value!==this._service&&he(this,"value-changed",{value:{service:e.detail.value||""}})}};e([ie({type:Object})],Oe.prototype,"hass",void 0),e([ie({type:String})],Oe.prototype,"entity_id",void 0),e([ie({type:Object})],Oe.prototype,"config",void 0),e([ie({type:Boolean})],Oe.prototype,"expose_by_default",void 0),e([ie({type:String})],Oe.prototype,"type",void 0),e([oe()],Oe.prototype,"_curIndex",void 0),e([oe()],Oe.prototype,"_customActions",void 0),e([oe()],Oe.prototype,"_remainActions",void 0),e([oe()],Oe.prototype,"_actionDetail",void 0),e([oe()],Oe.prototype,"_action",void 0),e([oe()],Oe.prototype,"_service",void 0),e([oe()],Oe.prototype,"_serviceData",void 0),e([oe()],Oe.prototype,"_responseData",void 0),Oe=e([ee("clova-info-detail")],Oe);let Ge=class extends(_e(ue(pe(Y)))){constructor(){super(...arguments),this._tap=["basic","detail"],this._curTabIndex=0}_update(e){var t,i,o,n;this.config={entity_config:(null===(i=null===(t=e.data.clova_config)||void 0===t?void 0:t.entity_config)||void 0===i?void 0:i[this.entity_id])||{},default_config:this.config.default_config||{}},this.title=(null===(n=null===(o=this.config.entity_config)||void 0===o?void 0:o.name)||void 0===n?void 0:n.toString())||this.hass.states[this.entity_id].attributes.friendly_name||""}async showDialog(e,t,i=!1){var o,n;this.title=e,this.large=i,this.open=!0,this.config={entity_config:(null===(o=t.config)||void 0===o?void 0:o.entity_config)||{},default_config:(null===(n=t.config)||void 0===n?void 0:n.default_config)||{}},this.expose_by_default=t.expose_by_default,this.entity_id=t.entity_id,this._card=this._makeCard(),void 0===this._event_listenser&&se().addEventListener("clova-updated",this._event_listenser=e=>this._updated(e))}closeDialog(){var e;(null===(e=history.state)||void 0===e?void 0:e.ClovaPopup)&&history.back()}closePopup(){this.open=!1,this._curTabIndex=0,this.title="",this.entity_id="",this.config={entity_config:{},default_config:{}},this.expose_by_default=void 0,void 0!==this._event_listenser&&(se().removeEventListener("clova-updated",this._event_listenser),this._event_listenser=void 0)}_makeCard(){let e=this._tap[this._curTabIndex],t=document.createElement(`clova-info-${e}`);return t.hass=this.hass,t.config={entity_config:this.config.entity_config||{},default_config:this.config.default_config||{}},t.expose_by_default=this.expose_by_default||!0,t.entity_id=this.entity_id,t.type=this._getType(),t}_getType(){var e,t;return((null===(e=this.config.entity_config)||void 0===e?void 0:e.type)||(null===(t=this.config.default_config)||void 0===t?void 0:t.type)||"").toUpperCase()}_enlarge(){this.large=!this.large}render(){return this.open?R`
			<ha-dialog
				open
				@closed=${this.closeDialog}
				.heading=${!0}
				hideActions
			>
				<div slot="heading" class="heading">
					<ha-header-bar>
						<ha-icon-button
							slot="navigationIcon"
							dialogAction="cancel"
							.label=${re("title")}
							.path=${me}
						></ha-icon-button>
						<div
							slot="title"
							class="main-title"
							.title=${this.title}
							@click=${this._enlarge}
						>
							${this.title}
						</div>
					</ha-header-bar>
					<mwc-tab-bar
						.activeIndex=${this._curTabIndex}
						@MDCTabBar:activated=${this._handleTabActivated}
					>
						${this._tap.map((e=>R`
							<mwc-tab .label=${re(`panel.label.${e}`)}></mwc-tab>
						`))}
					</mwc-tab-bar>
				</div>
				<div class="content">
					${this._card}
				</div>
			</ha-dialog>
		`:R``}static get styles(){return a`
			ha-dialog {
				--dialog-surface-position: static;
				--dialog-content-position: static;
			}

			ha-header-bar {
				--mdc-theme-on-primary: var(--primary-text-color);
				--mdc-theme-primary: var(--mdc-theme-surface);
				flex-shrink: 0;
				display: block;
			}

			@media all and (max-width: 450px), all and (max-height: 500px) {
			  ha-header-bar {
				--mdc-theme-primary: var(--app-header-background-color);
				--mdc-theme-on-primary: var(--app-header-text-color, white);
				border-bottom: none;
			  }
			}

			.heading {
			  border-bottom: 1px solid
				var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
			}

			@media all and (min-width: 451px) and (min-height: 501px) {
				ha-dialog {
					--mdc-dialog-max-width: 90vw;
				}

				ha-header-bar {
					width: 400px;
				}

				.main-title {
					overflow: hidden;
					text-overflow: ellipsis;
					cursor: default;
				}

				:host([large]) .content {
					width: calc(90vw - 48px);
				}
			}
			@media all and (max-width: 450px), all and (max-height: 500px) {
				ha-dialog {
					--mdc-dialog-min-width: 100vw;
					--mdc-dialog-max-width: 100vw;
					--mdc-dialog-min-height: 100%;
					--mdc-dialog-max-height: 100%;
					--mdc-shape-medium: 0px;
					--vertial-align-dialog: flex-end;
				}
			}
		`}_handleTabActivated(e){this._curTabIndex=e.detail.index||0,this._card=this._makeCard()}};e([ie({type:Object})],Ge.prototype,"hass",void 0),e([ie({type:Boolean})],Ge.prototype,"open",void 0),e([ie({reflect:!0,type:Boolean})],Ge.prototype,"large",void 0),e([ie({type:String})],Ge.prototype,"entity_id",void 0),e([ie({type:Object})],Ge.prototype,"config",void 0),e([ie({type:Boolean})],Ge.prototype,"expose_by_default",void 0),e([oe()],Ge.prototype,"_tap",void 0),e([oe()],Ge.prototype,"_curTabIndex",void 0),e([oe()],Ge.prototype,"_card",void 0),Ge=e([ee("clova-popup")],Ge);let ke=class extends(ve(pe(Y))){updated(e){var t;super.updated(e),null===(t=this.HaCard)||void 0===t||t.forEach((e=>{let t=e.clientWidth-e.querySelector("div.expose").clientWidth-24;e.querySelector("div.info").querySelectorAll("div").forEach((e=>{e.style.setProperty("max-width",`${t}px`)}))}))}connectedCallback(){super.connectedCallback(),this._default_setting()}async _default_setting(){await(async()=>{await ae().loadBackendTranslation("title"),await ae().loadBackendTranslation("type"),await ae().loadBackendTranslation("action"),await ae().loadBackendTranslation("panel")})(),await(async()=>{customElements.get("developer-tools-event")||await de();const e=document.createElement("developer-tools-router");await e.routerOptions.routes.event.load()})(),await(async()=>{customElements.get("developer-tools-event")||await de();const e=document.createElement("developer-tools-router");await e.routerOptions.routes.service.load()})()}_connect(e){this._ws_id||(this._ws_id=e.id),this._clova_config=e.data.clova_config||{},this._default_config=e.data.default_config||{}}_update(e){this._clova_config=e.data.clova_config||{}}_toggleChanged(e){let t=e.target;this._ws_connection.sendMessage({type:"clova/update",entity_id:t.entity_id,key:"expose",value:t.checked})}_popup_info_card(e){var t,i,o,n;let a=e.target;ce(a.title,{type:"basic",entity_id:a.entity_id,config:{entity_config:(null===(i=null===(t=this._clova_config)||void 0===t?void 0:t.entity_config)||void 0===i?void 0:i[a.entity_id])||{},default_config:(null===(o=this._default_config)||void 0===o?void 0:o[a.entity_id])||{}},expose_by_default:(null===(n=this._clova_config)||void 0===n?void 0:n.expose_by_default)||!0})}render(){var e,t;let i=this.hass.states,o=(null===(e=this._clova_config)||void 0===e?void 0:e.entity_config)||{},n=Object.keys(o),a=(null===(t=this._clova_config)||void 0===t?void 0:t.expose_by_default)||!0;return R`
      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title>${this.hass.localize("component.clova.title")}</div>
          </app-toolbar>
        </app-header>
        <div class="content">
        ${n.map((e=>{var t;const n=o[e];return e in i?R`
            <ha-card outlined>
              <div class="header">
                <div class="info">
                  <div class="primary name">
                    ${(null===(t=null==n?void 0:n.name)||void 0===t?void 0:t.toString())||i[e].attributes.friendly_name}
                  </div>
                  <div class="secondary">
                    ${e}
                  </div>
                </div>
                <div class="expose">
                  <ha-switch
                    .checked=${n.hasOwnProperty("expose")?n.expose:a}
                    .entity_id = ${e}
                    @change=${this._toggleChanged}
                  ></ha-switch>
                </div>
              </div>
              <div class="action">
                <mwc-button
                  @click=${this._popup_info_card}
                  label=${re("panel.label.edit")}
                  .title=${(null==n?void 0:n.name)||i[e].attributes.friendly_name}
                  .entity_id=${e}
                ></mwc-button>
              </div>
            </ha-card>
        `:""}))}
			  </div>
      </ha-app-layout>
		`}static get styles(){return a`
			:host {
				font-family: var(--paper-font-subhead_-_font-family);
				-webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
				font-size: var(--paper-font-subhead_-_font-size);
				font-weight: var(--paper-font-subhead_-_font-weight);
				line-height: var(--paper-font-subhead_-_line-height);
			}
			app-toolbar {
				display: flex;
				align-items: center;
				font-size: 20px;
				height: var(--header-height);
				padding: 0px 16px;
				pointer-events: none;
				background-color: var(--app-header-background-color);
				font-weight: 400;
				color: var(--app-header-text-color, white);
				border-bottom: var(--app-header-border-bottom, none);
				box-sizing: border-box;
			}
			.content {
				display: grid;
				grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
				gap: 16px;
				padding: 8px 16px 16px;
				margin-bottom: 64px;
			}
			.header {
				display: flex;
				position: relative;
				padding: 0px 8px 8px 16px;
			}
			.header .info {
				flex: 1 1 0%;
				align-self: center;
			}
			.header .info div {
				overflow-wrap: break-word;
				display: -webkit-box;
				-webkit-box-orient: vertical;
				-webkit-line-clamp: 1;
				overflow: hidden;
				text-overflow: ellipsis;
			}
			.primary {
				font-size: 16px;
				margin-top: 16px;
				margin-right: 2px;
				font-weight: 600;
				word-break: break-word;
				color: var(--primary-color);
			}
			.secondary {
				font-size: 14px;
				color: var(--secondary-text-color);
			}
			.expose {
				min-height: 35px;
				margin-top: 16px;
				display: var(--layout-horizontal_-_display);
				-webkit-align-items: var(--layout-center_-_-webkit-align-items);
				align-items: var(--layout-center_-_align-items);
			}
		`}};e([ie({type:Object})],ke.prototype,"hass",void 0),e([ie({type:Boolean})],ke.prototype,"narrow",void 0),e([ie({type:Object})],ke.prototype,"route",void 0),e([ie({type:Object})],ke.prototype,"panel",void 0),e([function(e){return ne({descriptor:t=>({get(){var t,i;return null!==(i=null===(t=this.renderRoot)||void 0===t?void 0:t.querySelectorAll(e))&&void 0!==i?i:[]},enumerable:!0,configurable:!0})})}("ha-card")],ke.prototype,"HaCard",void 0),e([oe()],ke.prototype,"_clova_config",void 0),e([oe()],ke.prototype,"_default_config",void 0),ke=e([ee("clova-panel")],ke);
