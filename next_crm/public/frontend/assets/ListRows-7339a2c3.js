import{l as B,k as R,j as b,u as r,b as s,c as a,F as d,f as _,d as y,w as l,e as f,t as p,g as n,G as A,p as C,O as v,P as w,Q as k}from"./index-8ca2d158.js";import{h as N,g as h,i as P,f as V}from"./ListBulkActions-ccdc1c2a.js";const D={key:0,class:"mx-3 mt-2 h-full overflow-y-auto sm:mx-5"},E={class:"my-2 flex items-center gap-2 text-base font-medium text-gray-800"},F={class:"flex items-center gap-1"},G={key:1,class:"text-gray-500"},L={key:2},z={__name:"ListRows",props:{rows:{type:Array,required:!0}},setup(g){const i=g,c=B(i.rows);R(()=>i.rows,t=>c.value=t);let x=b(()=>i.rows.every(t=>t.group&&t.rows&&Array.isArray(t.rows)));return(t,S)=>r(x)?(s(),a("div",D,[(s(!0),a(d,null,_(c.value,e=>(s(),a("div",{key:e.group},[y(r(N),{group:e},{default:l(()=>[f("div",E,[f("div",null,p(t.__(e.label))+" -",1),f("div",F,[e.icon?(s(),n(A(e.icon),{key:0})):C("",!0),e.group==" "?(s(),a("div",G,p(t.__("Empty")),1)):(s(),a("div",L,p(e.group),1))])])]),_:2},1032,["group"]),y(r(P),{group:e,id:"list-rows"},{default:l(()=>[(s(!0),a(d,null,_(e.rows,o=>(s(),n(r(h),{key:o.name,row:o},{default:l(({idx:u,column:m,item:$})=>[v(t.$slots,"default",w(k({idx:u,column:m,item:$,row:o})))]),_:2},1032,["row"]))),128))]),_:2},1032,["group"])]))),128))])):(s(),n(r(V),{key:1,class:"mx-3 sm:mx-5",id:"list-rows"},{default:l(()=>[(s(!0),a(d,null,_(c.value,e=>(s(),n(r(h),{key:e.name,row:e},{default:l(({idx:o,column:u,item:m})=>[v(t.$slots,"default",w(k({idx:o,column:u,item:m,row:e})))]),_:2},1032,["row"]))),128))]),_:3}))}};export{z as _};
//# sourceMappingURL=ListRows-7339a2c3.js.map
