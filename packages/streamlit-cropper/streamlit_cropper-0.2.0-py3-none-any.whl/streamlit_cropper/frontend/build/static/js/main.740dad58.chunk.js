/*! For license information please see main.740dad58.chunk.js.LICENSE.txt */
(this.webpackJsonpstreamlit_component_template=this.webpackJsonpstreamlit_component_template||[]).push([[0],{22:function(e,t,n){e.exports=n(38)},35:function(e,t){},36:function(e,t){},37:function(e,t){},38:function(e,t,n){"use strict";n.r(t);var a,r=n(9),o=n.n(r),s=n(19),i=n.n(s),l=n(7),c=n(0),u=n(3),d=n(1),m=n(2),h=n(20),g=n.n(h),f=n(6),v=n(21),E=n(13),b=function(){function e(t,n,a,r){var o=this;Object(c.a)(this,e),this.dataTable=void 0,this.indexTable=void 0,this.columnsTable=void 0,this.styler=void 0,this.getCell=function(e,t){var n=e<o.headerRows&&t<o.headerColumns,a=e>=o.headerRows&&t<o.headerColumns,r=e<o.headerRows&&t>=o.headerColumns;if(n){var s=["blank"];return t>0&&s.push("level"+e),{type:"blank",classNames:s.join(" "),content:""}}if(r){var i=t-o.headerColumns;return{type:"columns",classNames:["col_heading","level"+e,"col"+i].join(" "),content:o.getContent(o.columnsTable,i,e)}}if(a){var l=e-o.headerRows,c=["row_heading","level"+t,"row"+l];return{type:"index",id:"T_".concat(o.uuid,"level").concat(t,"_row").concat(l),classNames:c.join(" "),content:o.getContent(o.indexTable,l,t)}}var u=e-o.headerRows,d=t-o.headerColumns,m=["data","row"+u,"col"+d],h=o.styler?o.getContent(o.styler.displayValuesTable,u,d):o.getContent(o.dataTable,u,d);return{type:"data",id:"T_".concat(o.uuid,"row").concat(u,"_col").concat(d),classNames:m.join(" "),content:h}},this.getContent=function(e,t,n){var a=e.getColumnAt(n);if(null===a)return"";switch(o.getColumnTypeId(e,n)){case E.b.Timestamp:return o.nanosToDate(a.get(t));default:return a.get(t)}},this.dataTable=E.a.from(t),this.indexTable=E.a.from(n),this.columnsTable=E.a.from(a),this.styler=r?{caption:r.get("caption"),displayValuesTable:E.a.from(r.get("displayValues")),styles:r.get("styles"),uuid:r.get("uuid")}:void 0}return Object(u.a)(e,[{key:"getColumnTypeId",value:function(e,t){return e.schema.fields[t].type.typeId}},{key:"nanosToDate",value:function(e){return new Date(e/1e6)}},{key:"rows",get:function(){return this.indexTable.length+this.columnsTable.numCols}},{key:"columns",get:function(){return this.indexTable.numCols+this.columnsTable.length}},{key:"headerRows",get:function(){return this.rows-this.dataRows}},{key:"headerColumns",get:function(){return this.columns-this.dataColumns}},{key:"dataRows",get:function(){return this.dataTable.length}},{key:"dataColumns",get:function(){return this.dataTable.numCols}},{key:"uuid",get:function(){return this.styler&&this.styler.uuid}},{key:"caption",get:function(){return this.styler&&this.styler.caption}},{key:"styles",get:function(){return this.styler&&this.styler.styles}},{key:"table",get:function(){return this.dataTable}},{key:"index",get:function(){return this.indexTable}},{key:"columnTable",get:function(){return this.columnsTable}}]),e}();!function(e){e.COMPONENT_READY="streamlit:componentReady",e.SET_COMPONENT_VALUE="streamlit:setComponentValue",e.SET_FRAME_HEIGHT="streamlit:setFrameHeight"}(a||(a={}));var p=function e(){Object(c.a)(this,e)};p.API_VERSION=1,p.RENDER_EVENT="streamlit:render",p.events=new v.a,p.registeredMessageListener=!1,p.lastFrameHeight=void 0,p.setComponentReady=function(){p.registeredMessageListener||(window.addEventListener("message",p.onMessageEvent),p.registeredMessageListener=!0),p.sendBackMsg(a.COMPONENT_READY,{apiVersion:p.API_VERSION})},p.setFrameHeight=function(e){void 0===e&&(e=document.body.scrollHeight),e!==p.lastFrameHeight&&(p.lastFrameHeight=e,p.sendBackMsg(a.SET_FRAME_HEIGHT,{height:e}))},p.setComponentValue=function(e){p.sendBackMsg(a.SET_COMPONENT_VALUE,{value:e})},p.onMessageEvent=function(e){switch(e.data.type){case p.RENDER_EVENT:p.onRenderMessage(e.data)}},p.onRenderMessage=function(e){var t=e.args;null==t&&(console.error("Got null args in onRenderMessage. This should never happen"),t={});var n=e.dfs&&e.dfs.length>0?p.argsDataframeToObject(e.dfs):{};t=Object(f.a)(Object(f.a)({},t),n);var a=Boolean(e.disabled),r=new CustomEvent(p.RENDER_EVENT,{detail:{disabled:a,args:t}});p.events.dispatchEvent(r)},p.argsDataframeToObject=function(e){var t=e.map((function(e){var t=e.key,n=e.value;return[t,p.toArrowTable(n)]}));return Object.fromEntries(t)},p.toArrowTable=function(e){var t=e.data,n=t.data,a=t.index,r=t.columns;return new b(n,a,r)},p.sendBackMsg=function(e,t){window.parent.postMessage(Object(f.a)({isStreamlitMessage:!0,type:e},t),"*")};o.a.PureComponent;var T=n(17),y=function(e){var t=function(t){Object(d.a)(a,t);var n=Object(m.a)(a);function a(t){var r;return Object(c.a)(this,a),(r=n.call(this,t)).componentDidMount=function(){p.events.addEventListener(p.RENDER_EVENT,r.onRenderEvent),p.setComponentReady()},r.componentDidUpdate=function(){null!=r.state.componentError&&p.setFrameHeight()},r.componentWillUnmount=function(){p.events.removeEventListener(p.RENDER_EVENT,r.onRenderEvent)},r.onRenderEvent=function(e){var t=e;r.setState({renderData:t.detail})},r.render=function(){return null!=r.state.componentError?o.a.createElement("div",null,o.a.createElement("h1",null,"Component Error"),o.a.createElement("span",null,r.state.componentError.message)):null==r.state.renderData?null:o.a.createElement(e,{width:window.innerWidth,disabled:r.state.renderData.disabled,args:r.state.renderData.args})},r.state={renderData:void 0,componentError:void 0},r}return a}(o.a.PureComponent);return t.getDerivedStateFromError=function(e){return{componentError:e}},g()(t,e)}((function(e){var t=Object(r.useState)(new T.fabric.Canvas("")),n=Object(l.a)(t,2),a=n[0],s=n[1],i=e.args,c=i.canvasWidth,u=i.canvasHeight,d=i.imageData,m=document.createElement("canvas"),h=m.getContext("2d");if(m.width=c,m.height=u,h){var g=h.createImageData(c,u);g.data.set(d),h.putImageData(g,0,0);var f=m.toDataURL()}else f="";return Object(r.useEffect)((function(){var t=e.args,n=t.rectTop,a=t.rectLeft,r=t.rectWidth,o=t.rectHeight,i=t.boxColor,l=t.lockAspect,c=new T.fabric.Canvas("c",{enableRetinaScaling:!1,backgroundImage:f,uniScaleTransform:l}),u=new T.fabric.Rect({left:a,top:n,fill:"",width:r,height:o,objectCaching:!0,stroke:i,strokeWidth:3,hasRotatingPoint:!1});c.add(u),s(c),p.setFrameHeight()}),[u,c]),Object(r.useEffect)((function(){var t=e.args.realtimeUpdate;if(a){var n=function(){a.renderAll();var e=a.getObjects()[0].getBoundingRect();p.setComponentValue({coords:e})};return t?(a.on("object:modified",n),function(){a.off("object:modified")}):(a.on("mouse:dblclick",n),function(){a.off("mouse:dblclick")})}})),o.a.createElement(o.a.Fragment,null,o.a.createElement("canvas",{id:"c",width:c,height:u}))}));i.a.render(o.a.createElement(o.a.StrictMode,null,o.a.createElement(y,null)),document.getElementById("root"))}},[[22,1,2]]]);
//# sourceMappingURL=main.740dad58.chunk.js.map