import{_ as E,a as I}from"./ViewControls-5fb3bbce.js";import{_ as R}from"./CustomActions-d5b79d4f.js";import{C as D}from"./CustomersIcon-c98fca89.js";import{_ as j}from"./LayoutHeader-72a3cdee.js";import{_ as S}from"./CustomerModal-0ca69a84.js";import{_ as H}from"./QuickEntryModal-ebc5f118.js";import{m as h,h as O,i as q,j as A,s as J,k as Q,l as y,r as L,b as i,c,d as a,w as u,u as p,F,f as N,g as C,n as P,p as b,e as B,t as z,q as G}from"./index-8ca2d158.js";import{_ as K,H as T,a as X,f as Y,b as Z,g as ee,c as te,d as le,e as oe}from"./ListBulkActions-ccdc1c2a.js";import{b as ae,_ as se,w as ne,h as ie,d as ue,t as re,c as de}from"./index-b1bb6af7.js";import{_ as me}from"./Dropdown.vue_vue_type_script_setup_true_lang-dba778cd.js";import{_ as pe}from"./ListFooter-ed664a38.js";import"./FadedScrollableDiv-10ee6cf2.js";import"./IconPicker-b2d84813.js";import"./views-5d4a0486.js";import"./DatePicker-0e72d67e.js";import"./PinIcon-0747ea14.js";import"./settings-9f3d7d3a.js";import"./DetailsIcon-14f9b41c.js";import"./DragVerticalIcon-523c4542.js";import"./Fields-02fbbc9b.js";import"./IndicatorIcon-367a8d49.js";import"./AddressModal-e11ac707.js";import"./WebsiteIcon-326f696e.js";import"./Switch.vue_vue_type_script_setup_true_lang-cbc97d13.js";import"./AssignmentModal-759f92c3.js";const fe={key:0},ve=["onClick"],ce={key:1},ye={key:2},ke=["onClick"],Ce={__name:"CustomersListView",props:h({rows:{type:Array,required:!0},columns:{type:Array,required:!0},options:{type:Object,default:()=>({selectable:!0,showTooltip:!0,resizeColumn:!1,totalCount:0,rowCount:0})}},{modelValue:{},modelModifiers:{},list:{},listModifiers:{}}),emits:h(["loadMore","updatePageCount","columnWidthUpdated","applyFilter","applyLikeFilter","likeDoc"],["update:modelValue","update:list"]),setup(d,{expose:$,emit:V}){const m=V,s=O(),_=q(d,"modelValue"),g=q(d,"list"),x=A(()=>{var e,l;return!!((l=(e=g.value.params)==null?void 0:e.filters)!=null&&l._liked_by)}),{user:k}=J();function U(e){if(e)return JSON.parse(e).includes(k)}Q(_,(e,l)=>{e!==l&&m("updatePageCount",e)});const f=y(null);return $({customListActions:A(()=>{var e;return(e=f.value)==null?void 0:e.customListActions})}),(e,l)=>{const r=L("Button"),t=L("FormControl");return i(),c(F,null,[a(p(le),{columns:d.columns,rows:d.rows,options:{getRowRoute:o=>({name:"Customer",params:{customerId:o.name},query:{view:p(s).query.view,viewType:p(s).params.viewType}}),selectable:d.options.selectable,showTooltip:d.options.showTooltip,resizeColumn:d.options.resizeColumn},"row-key":"name"},{default:u(()=>[a(p(K),{class:"sm:mx-5 mx-3",onColumnWidthUpdated:l[1]||(l[1]=o=>m("columnWidthUpdated"))},{default:u(()=>[(i(!0),c(F,null,N(d.columns,o=>(i(),C(p(X),{key:o.key,item:o,onColumnWidthUpdated:n=>m("columnWidthUpdated",o)},{default:u(()=>[o.key=="_liked_by"?(i(),C(r,{key:0,variant:"ghosted",class:P(["!h-4",x.value?"fill-red-500":"fill-white"]),onClick:l[0]||(l[0]=()=>m("applyLikeFilter"))},{default:u(()=>[a(T,{class:"h-4 w-4"})]),_:1},8,["class"])):b("",!0)]),_:2},1032,["item","onColumnWidthUpdated"]))),128))]),_:1}),a(p(Y),{class:"mx-3 sm:mx-5",id:"list-rows"},{default:u(()=>[(i(!0),c(F,null,N(d.rows,o=>(i(),C(p(ee),{key:o.name,row:o},{default:u(({idx:n,column:w,item:v})=>[a(p(Z),{item:v},{prefix:u(()=>[w.key==="customer_name"?(i(),c("div",fe,[v.label?(i(),C(p(ae),{key:0,class:"flex items-center",image:v.logo,label:v.label,size:"sm"},null,8,["image","label"])):b("",!0)])):b("",!0)]),default:u(({label:W})=>[["modified","creation"].includes(w.key)?(i(),c("div",{key:0,class:"truncate text-base",onClick:M=>m("applyFilter",{event:M,idx:n,column:w,item:v,firstColumn:d.columns[0]})},[a(p(se),{text:v.label},{default:u(()=>[B("div",null,z(v.timeAgo),1)]),_:2},1032,["text"])],8,ve)):w.type==="Check"?(i(),c("div",ce,[a(t,{type:"checkbox",modelValue:v,disabled:!0,class:"text-gray-900"},null,8,["modelValue"])])):w.key==="_liked_by"?(i(),c("div",ye,[w.key=="_liked_by"?(i(),C(r,{key:0,variant:"ghosted",class:P(U(v)?"fill-red-500":"fill-white"),onClick:G(()=>m("likeDoc",{name:o.name,liked:U(v)}),["stop","prevent"])},{default:u(()=>[a(T,{class:"h-4 w-4"})]),_:2},1032,["class","onClick"])):b("",!0)])):(i(),c("div",{key:3,class:"truncate text-base",onClick:M=>m("applyFilter",{event:M,idx:n,column:w,item:v,firstColumn:d.columns[0]})},z(W),9,ke))]),_:2},1032,["item"])]),_:2},1032,["row"]))),128))]),_:1}),a(p(te),null,{actions:u(({selections:o,unselectAll:n})=>[a(p(me),{options:f.value.bulkActions(o,n)},{default:u(()=>[a(r,{icon:"more-horizontal",variant:"ghost"})]),_:2},1032,["options"])]),_:1})]),_:1},8,["columns","rows","options"]),a(p(pe),{class:"border-t sm:px-5 px-3 py-2",modelValue:_.value,"onUpdate:modelValue":l[2]||(l[2]=o=>_.value=o),options:{rowCount:d.options.rowCount,totalCount:d.options.totalCount},onLoadMore:l[3]||(l[3]=o=>m("loadMore"))},null,8,["modelValue","options"]),a(oe,{ref_key:"listBulkActionsRef",ref:f,modelValue:g.value,"onUpdate:modelValue":l[4]||(l[4]=o=>g.value=o),doctype:"Customer",options:{hideAssign:!0}},null,8,["modelValue"])],64)}}},_e={key:1,class:"flex h-full items-center justify-center"},ge={class:"flex flex-col items-center gap-3 text-xl font-medium text-gray-500"},Oe={__name:"Customers",setup(d){const $=y(null),V=y(!1),m=y(!1),s=y({}),_=y(1),g=y(1),x=y(20),k=y(null),U=A(()=>{var f,e,l;return!((e=(f=s.value)==null?void 0:f.data)!=null&&e.data)||!["list","group_by"].includes(s.value.data.view_type)?[]:(l=s.value)==null?void 0:l.data.data.map(r=>{var o;let t={};return(o=s.value)==null||o.data.rows.forEach(n=>{t[n]=r[n],n==="customer_name"?t[n]={label:r.customer_name,logo:r.image}:n==="website"?t[n]=ne(r.website):n==="annual_revenue"?t[n]=ie(r.annual_revenue,r.currency):["modified","creation"].includes(n)&&(t[n]={label:ue(r[n],de),timeAgo:__(re(r[n]))})}),t})});return(f,e)=>{const l=L("FeatherIcon"),r=L("Button");return i(),c(F,null,[a(j,null,{"left-header":u(()=>[a(I,{modelValue:k.value,"onUpdate:modelValue":e[0]||(e[0]=t=>k.value=t),routeName:"Customers"},null,8,["modelValue"])]),"right-header":u(()=>{var t;return[(t=$.value)!=null&&t.customListActions?(i(),C(R,{key:0,actions:$.value.customListActions},null,8,["actions"])):b("",!0),a(r,{variant:"solid",label:f.__("Create"),onClick:e[1]||(e[1]=o=>V.value=!0)},{prefix:u(()=>[a(l,{name:"plus",class:"h-4"})]),_:1},8,["label"])]}),_:1}),a(E,{ref_key:"viewControls",ref:k,modelValue:s.value,"onUpdate:modelValue":e[2]||(e[2]=t=>s.value=t),loadMore:_.value,"onUpdate:loadMore":e[3]||(e[3]=t=>_.value=t),resizeColumn:g.value,"onUpdate:resizeColumn":e[4]||(e[4]=t=>g.value=t),updatedPageCount:x.value,"onUpdate:updatedPageCount":e[5]||(e[5]=t=>x.value=t),doctype:"Customer"},null,8,["modelValue","loadMore","resizeColumn","updatedPageCount"]),s.value.data&&U.value.length?(i(),C(Ce,{key:0,ref_key:"customersListView",ref:$,modelValue:s.value.data.page_length_count,"onUpdate:modelValue":e[6]||(e[6]=t=>s.value.data.page_length_count=t),list:s.value,"onUpdate:list":e[7]||(e[7]=t=>s.value=t),rows:U.value,columns:s.value.data.columns,options:{showTooltip:!1,resizeColumn:!0,rowCount:s.value.data.row_count,totalCount:s.value.data.total_count},onLoadMore:e[8]||(e[8]=()=>_.value++),onColumnWidthUpdated:e[9]||(e[9]=()=>g.value++),onUpdatePageCount:e[10]||(e[10]=t=>x.value=t),onApplyFilter:e[11]||(e[11]=t=>k.value.applyFilter(t)),onApplyLikeFilter:e[12]||(e[12]=t=>k.value.applyLikeFilter(t)),onLikeDoc:e[13]||(e[13]=t=>k.value.likeDoc(t))},null,8,["modelValue","list","rows","columns","options"])):s.value.data?(i(),c("div",_e,[B("div",ge,[a(D,{class:"h-10 w-10"}),B("span",null,z(f.__("No {0} Found",[f.__("Customers")])),1),a(r,{label:f.__("Create"),onClick:e[14]||(e[14]=t=>V.value=!0)},{prefix:u(()=>[a(l,{name:"plus",class:"h-4"})]),_:1},8,["label"])])])):b("",!0),a(S,{modelValue:V.value,"onUpdate:modelValue":e[15]||(e[15]=t=>V.value=t),quickEntry:m.value,"onUpdate:quickEntry":e[16]||(e[16]=t=>m.value=t)},null,8,["modelValue","quickEntry"]),m.value?(i(),C(H,{key:2,modelValue:m.value,"onUpdate:modelValue":e[17]||(e[17]=t=>m.value=t),doctype:"Customer"},null,8,["modelValue"])):b("",!0)],64)}}};export{Oe as default};
//# sourceMappingURL=Customers-429fc749.js.map
