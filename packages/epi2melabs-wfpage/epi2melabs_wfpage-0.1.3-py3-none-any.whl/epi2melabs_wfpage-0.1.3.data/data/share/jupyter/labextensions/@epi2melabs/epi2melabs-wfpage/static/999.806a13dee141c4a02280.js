(self.webpackChunk_epi2melabs_epi2melabs_wfpage=self.webpackChunk_epi2melabs_epi2melabs_wfpage||[]).push([[999],{3730:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>Y});var a=n(2233),r=n(4026),o=n(5215),s=n(3086);const l=new(n(7563).LabIcon)({name:"ui-components:labs",svgstr:'\n  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="42" height="51" viewBox="0 0 42 51">\n    <defs>\n        <filter id="Rectangle_1" x="0" y="0" width="42" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n        <filter id="Rectangle_2" x="0" y="24" width="42" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-2"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-2"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n        <filter id="Rectangle_3" x="0" y="12" width="28" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-3"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-3"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n    </defs>\n    <g id="Component_2_1" data-name="Component 2 – 1" transform="translate(9 6)">\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_1)">\n        <rect id="Rectangle_1-2" data-name="Rectangle 1" width="24" height="9" rx="1" transform="translate(9 6)" fill="#08bbb2"/>\n        </g>\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_2)">\n        <rect id="Rectangle_2-2" data-name="Rectangle 2" width="24" height="9" rx="1" transform="translate(9 30)" fill="#0179a4"/>\n        </g>\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_3)">\n        <rect id="Rectangle_3-2" data-name="Rectangle 3" width="10" height="9" rx="1" transform="translate(9 18)" fill="#fccb10"/>\n        </g>\n    </g>\n  </svg>\n'});var i=n(6271),c=n.n(i),d=n(974),p=n(3839),m=n.n(p);const u={UNKNOWN:{name:"UNKNOWN",className:"grey"},LAUNCHED:{name:"LAUNCHED",className:"blue"},ENCOUNTERED_ERROR:{name:"ENCOUNTERED_ERROR",className:"orange"},COMPLETED_SUCCESSFULLY:{name:"COMPLETED_SUCCESSFULLY",className:"green"},TERMINATED:{name:"TERMINATED",className:"black"}},f=m()((({status:e,className:t})=>c().createElement("div",{className:`status-indicator ${t}`},c().createElement("div",{className:u[e].className}))))`
  > div {
    width: 18px;
    height: 18px;
    padding: 0;
    border-radius: 100%;
    line-height: 18px;
    text-align: center;
    font-size: 10px;
    color: white;
  }

  .blue {
    cursor: pointer;
    background-color: #005c75;
    box-shadow: 0 0 0 rgba(204, 169, 44, 0.4);
    animation: pulse-blue 2s infinite;
  }

  @keyframes pulse-blue {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(44, 119, 204, 0.4);
      box-shadow: 0 0 0 0 rgba(44, 119, 204, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(44, 119, 204, 0);
      box-shadow: 0 0 0 10px rgba(44, 119, 204, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(44, 119, 204, 0);
      box-shadow: 0 0 0 0 rgba(44, 119, 204, 0);
    }
  }

  .orange {
    cursor: pointer;
    background-color: #e34040;
    box-shadow: 0 0 0 rgba(23, 187, 117, 0.4);
    animation: pulse-orange 2s infinite;
  }

  @keyframes pulse-orange {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.4);
      box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(255, 140, 0, 0);
      box-shadow: 0 0 0 10px rgba(255, 140, 0, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(255, 140, 0, 0);
      box-shadow: 0 0 0 0 rgba(255, 140, 0, 0);
    }
  }

  .green {
    cursor: pointer;
    background-color: #17bb75;
    box-shadow: 0 0 0 rgba(23, 187, 117, 0.4);
    animation: pulse-green 2s infinite;
  }

  @keyframes pulse-green {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(23, 187, 117, 0.4);
      box-shadow: 0 0 0 0 rgba(23, 187, 117, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(23, 187, 117, 0);
      box-shadow: 0 0 0 10px rgba(23, 187, 117, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(23, 187, 117, 0);
      box-shadow: 0 0 0 0 rgba(23, 187, 117, 0);
    }
  }

  .grey {
    background-color: #707070;
  }

  .black {
    background-color: black;
  }
`;var g=n(2451),h=n(2978);async function b(e="",t={}){const n=h.ServerConnection.makeSettings(),a=g.URLExt.join(n.baseUrl,"epi2melabs-wfpage",e);let r;try{r=await h.ServerConnection.makeRequest(a,t,n)}catch(e){throw new h.ServerConnection.NetworkError(e)}let o=await r.text();if(o.length>0)try{o=JSON.parse(o)}catch(e){console.log("Not a JSON response body.",r)}if(!r.ok)throw new h.ServerConnection.ResponseError(r,o.message||o);return o}const x=m()((({className:e,docTrack:t})=>{const n=(0,d.useNavigate)(),a=(0,d.useParams)(),[r,o]=(0,i.useState)(),[s,l]=(0,i.useState)(""),[p,m]=(0,i.useState)({}),[u,g]=(0,i.useState)([]),[h,x]=(0,i.useState)([]),w=async()=>{const e=await b(`instances/${a.id}`);return o(e),l(e.status),e};(0,i.useEffect)((()=>{(async()=>{await w(),(async()=>{const{params:e}=await b(`params/${a.id}`);null!==e&&m(e)})(),E()})();const e=setInterval((()=>w()),5e3);return()=>{clearInterval(e)}}),[]);const E=async()=>{const{logs:e}=await b(`logs/${a.id}`);x(e)},k=async e=>{if(!e)return;const n=`${e.path}/output`;try{const e=await(await t.services.contents.get(n)).content.filter((e=>"directory"!==e.type));g(e)}catch(e){console.log("Instance outputs not available yet")}};(0,i.useEffect)((()=>{if(["COMPLETED_SUCCESSFULLY","TERMINATED","ENCOUNTERED_ERROR"].includes(s))return k(r),void E();{const e=setInterval((()=>k(r)),1e4),t=setInterval((()=>E()),7500);return()=>{k(r),E(),clearInterval(e),clearInterval(t)}}}),[s]);const v=async e=>{const t=await b(`instances/${a.id}`,{method:"DELETE",headers:{"Content-Type":"application/json"},body:JSON.stringify({delete:e})});e&&t.deleted&&n("/instances")},j=["LAUNCHED"].includes(s);return r?c().createElement("div",{className:`instance ${e}`},c().createElement("div",{className:"instance-container"},c().createElement("div",{className:"instance-section instance-header"},c().createElement("div",{className:"instance-header-top"},c().createElement("h2",{className:"instance-workflow"},"Workflow: ",r.workflow),j?c().createElement("button",{onClick:()=>v(!1)},"Stop Instance"):""),c().createElement("h1",null,"ID: ",a.id),c().createElement("div",{className:"instance-details"},c().createElement("div",{className:"instance-status"},c().createElement(f,{status:s||"UNKNOWN"}),c().createElement("p",null,s)),c().createElement("p",null,"Created: ",r.created_at),c().createElement("p",null,"Updated: ",r.updated_at))),c().createElement("div",{className:"instance-section instance-params"},c().createElement("h2",null,"Instance params"),c().createElement("div",{className:"instance-section-contents"},c().createElement("ul",null,Object.entries(p).map((([e,t])=>c().createElement("li",null,e,": ",t.toString())))))),c().createElement("div",{className:"instance-section instance-logs"},c().createElement("h2",null,"Instance logs"),c().createElement("div",{className:"instance-section-contents"},h?c().createElement("ul",null,h.map((e=>c().createElement("li",null,c().createElement("span",null,e))))):c().createElement("div",null,"Logs are loading..."))),c().createElement("div",{className:"instance-section instance-outputs"},c().createElement("h2",null,"Output files"),c().createElement("div",{className:"instance-section-contents"},u.length?c().createElement("ul",null,u.map((e=>c().createElement("li",null,c().createElement("button",{onClick:()=>{return n=e.path,void t.open(n);var n}},e.name))))):c().createElement("div",{className:"instance-section-contents"},"No outputs yet..."))),c().createElement("div",{className:"instance-section instance-delete"},c().createElement("h2",null,"Danger zone"),c().createElement("div",{className:"instance-section-contents"},c().createElement("div",{className:j?"inactive":"active"},c().createElement("button",{onClick:()=>j?null:v(!0)},"Delete Instance")))))):c().createElement("div",{className:`instance ${e}`},"Loading...")}))`
  background-color: #f6f6f6;

  .instance-container {
    padding: 50px 0 100px 0 !important;
  }

  .instance-section {
    width: 100%;
    padding: 15px;
    max-width: 1200px;
    margin: 0 auto 25px auto;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .instance-section > h2 {
    padding-bottom: 15px;
  }

  .instance-section-contents {
    padding: 15px;
    border-radius: 4px;
  }

  .instance-header-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
  }

  .instance-header-top h2 {
    padding-bottom: 15px;
  }

  .instance-header-top button {
    cursor: pointer;
    padding: 8px 15px;
    border: 1px solid #e34040;
    color: #e34040;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }

  .instance-header-top button:hover {
    cursor: pointer;
    background-color: #e34040;
    color: white;
  }

  .instance-details {
    display: flex;
    align-items: center;
  }

  .instance-details p {
    padding-left: 15px;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    color: rgba(0, 0, 0, 0.5);
  }

  .instance-status {
    display: flex;
    align-items: center;
  }

  .instance-status p {
    color: black;
    padding-left: 15px;
  }

  .instance-params .instance-section-contents {
    background-color: #f6f6f6;
  }

  .instance-params li {
    font-size: 12px;
    font-family: monospace;
  }

  .instance-logs .instance-section-contents {
    background-color: #f6f6f6;
    font-size: 12px;
    font-family: monospace;
    overflow: auto;
    text-overflow: initial;
    max-height: 500px;
    white-space: pre;
    color: black;
    border-radius: 4px;
  }

  .instance-logs .instance-section-contents span {
    font-size: 12px;
    font-family: monospace;
  }

  .instance-outputs li {
    margin: 0 0 5px 0;
    display: flex;
    background-color: #f6f6f6;
  }

  .instance-outputs button {
    width: 100%;
    text-align: left;
    padding: 5px;
    font-size: 12px;
    font-family: monospace;
    border: none;
    outline: none;
    background: transparent;
    border: 1px solid #f6f6f6;
  }

  .instance-outputs button:hover {
    border: 1px solid #005c75;
  }

  .instance-delete .instance-section-contents {
    background-color: #f6f6f6;
  }

  .instance-delete button {
    padding: 15px 25px;
    margin: 0 15px 0 0;
    border: 1px solid lightgray;
    color: lightgray;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }
  .instance-delete .active button {
    border: 1px solid #e34040;
    color: #e34040;
  }
  .instance-delete .active button:hover {
    cursor: pointer;
    background-color: #e34040;
    color: white;
  }
`;var w=n(7118),E=n.n(w),k=n(5894),v=n(2333),j=n(5205),y=n(7531);const N=m()((({id:e,label:t,format:n,description:a,defaultValue:r,error:o,onChange:s,className:l})=>{const[d,p]=(0,i.useState)(r);return c().createElement("div",{className:`BooleanInput ${l} ${d?"checked":"unchecked"}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("label",{htmlFor:e},c().createElement("input",{id:e,className:"boolInput",type:"checkbox",defaultChecked:r,onChange:t=>{p(t.target.value),s(e,n,!!t.target.checked)}}),c().createElement("span",null,"✓")),o?c().createElement("div",{className:"error"},c().createElement("p",null,"Error: ",o)):"")}))`
  .input-container {
    margin: 25px 0 0 0;
    padding: 25px;
    background-color: #1e1e1e;
    border-radius: 4px;
  }

  p {
    padding: 15px 0;
    margin: 0 0 10px 0;
  }

  label {
    padding: 15px 0 0 0;
    position: relative;
  }

  input {
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
  }

  label span {
    cursor: pointer;
    border: 0;
    padding: 0;
    margin: 0;
    transition: 0.2s ease-in-out all;
  }

  label span {
    margin-right: 15px;
    cursor: pointer;
    outline: none;
    background-color: transparent;
    padding: 10px 15px;
    border: 1px solid black;
    color: black;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    -moz-appearance: textfield;
  }

  label span {
    font-size: 20px;
  }

  input:checked + span {
    background-color: black;
    color: white;
  }

  .error {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,O=m()((({id:e,label:t,format:n,description:a,defaultValue:r,choices:o,error:s,onChange:l,className:i})=>c().createElement("div",{className:`SelectInput ${i}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("label",{htmlFor:e},c().createElement("select",{id:e,onChange:t=>l(e,n,t.target.value)},r?"":c().createElement("option",{className:"placeholder",selected:!0,disabled:!0,hidden:!0,value:"Select an option"},"Select an option"),o.map((e=>c().createElement("option",{key:e.label,selected:!(e.value!==r),value:e.value},e.label))))),s?c().createElement("div",{className:"error"},c().createElement("p",null,"Error: ",s)):"")))`
  .input-container {
    margin: 25px 0 0 0;
    padding: 25px;
    background-color: #1e1e1e;
    border-radius: 4px;
  }

  .input-container p {
    padding: 15px 0;
  }

  select {
    cursor: pointer;
    border: 0;
    padding: 0;
    margin: 0;
    transition: 0.2s ease-in-out all;
  }

  select {
    position: relative;
    cursor: pointer;
    outline: none;
    background-color: transparent;
    padding: 15px 25px;
    border: 1px solid black;
    color: black;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    /* for Firefox */
    appearance: none;
    -moz-appearance: none;
    /* for Chrome */
    -webkit-appearance: none;
  }

  .error {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,C=m()((({id:e,label:t,format:n,description:a,defaultValue:r,minLength:o,maxLength:s,pattern:l,error:i,onChange:d,className:p})=>c().createElement("div",{className:`TextInput ${p}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("label",{htmlFor:e},c().createElement("input",{id:e,type:"text",placeholder:"Enter a value",defaultValue:r,pattern:l,minLength:o,maxLength:s,onChange:t=>d(e,n,t.target.value)})),i?c().createElement("div",{className:"error"},c().createElement("p",null,"Error: ",i)):"")))`
  .input-container {
    margin: 25px 0 0 0;
    padding: 25px;
    background-color: #1e1e1e;
    border-radius: 4px;
  }

  .input-container p {
    padding: 15px 0;
  }

  input {
    border: 0;
    padding: 0;
    margin: 0;
    transition: 0.2s ease-in-out all;
  }
  input {
    min-width: 50%;
    margin-right: 15px;
    outline: none;
    background-color: transparent;
    padding: 15px 25px;
    border: 1px solid black;
    color: black;
    font-size: 11px;
    border-radius: 4px;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
  }

  .error {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,z=m()((({id:e,label:t,format:n,description:a,defaultValue:r,min:o,max:s,error:l,onChange:i,className:d})=>c().createElement("div",{className:`NumInput ${d}`},c().createElement("h4",null,t),c().createElement("p",null,a),c().createElement("label",{htmlFor:e},c().createElement("input",{id:e,type:"number",defaultValue:r,min:o,max:s,onChange:t=>i(e,n,Number(t.target.value))})),l?c().createElement("div",{className:"error"},c().createElement("p",null,"Error: ",l)):"")))`
  .input-container {
    margin: 25px 0 0 0;
    padding: 25px;
    background-color: #1e1e1e;
    border-radius: 4px;
  }

  .input-container p {
    padding: 15px 0;
  }

  input {
    cursor: pointer;
    border: 0;
    padding: 0;
    margin: 0;
    transition: 0.2s ease-in-out all;
  }
  input {
    margin-right: 15px;
    cursor: pointer;
    outline: none;
    background-color: transparent;
    padding: 15px 25px;
    border: 1px solid black;
    color: black;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;

    -moz-appearance: textfield;
  }
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
  }

  .error {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,S=(e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default}),R=m()((({id:e,schema:t,error:n,onChange:a,className:r})=>c().createElement("div",{className:`parameter ${r}`},((e,t,n,a)=>(e=>"boolean"===e.type)(t)?c().createElement(N,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default}))(e,t),{error:n,onChange:a})):(e=>!!e.enum)(t)?c().createElement(O,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default,choices:t.enum.map((e=>({value:e,label:e})))}))(e,t),{error:n,onChange:a})):(e=>"string"===e.type&&"file-path"===e.format)(t)||(e=>"string"===e.type&&!e.enum)(t)?c().createElement(C,Object.assign({},S(e,t),{error:n,onChange:a})):(e=>!!["integer","number"].includes(e.type))(t)?c().createElement(z,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default,min:t.minimum,max:t.maximum}))(e,t),{error:n,onChange:a})):c().createElement(C,Object.assign({},S(e,t),{error:n,onChange:a})))(e,t,n,a))))`
  padding: 25px 0;
  border-top: 1px solid #ccc;

  h4 {
    padding: 0 0 5px 0;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
  }

  p {
    padding: 0 0 10px 0;
  }

  input {
    font-size: 12px;
    font-family: monospace;
  }
`,_=m()((({title:e,fa_icon:t,properties:n,errors:a,onChange:r,className:o})=>{const[s,l]=(0,i.useState)(!1),d=0===Object.keys(a).length;k.library.add(j.fas,y.fab);const p=null==t?void 0:t.split(" ")[1],m=null==t?void 0:t.split(" ")[0],u=(null==p?void 0:p.startsWith("fa-"))?p.split("fa-")[1]:p;return c().createElement("div",{className:`parameter-section ${o}`},c().createElement("div",{className:"parameter-section-container "+(d?"valid":"")},c().createElement("button",{onClick:()=>l(!s)},c().createElement("h3",null,"string"==typeof t?c().createElement(v.FontAwesomeIcon,{icon:[m,u]}):"",e),c().createElement("div",null,c().createElement(v.FontAwesomeIcon,{icon:j.faCaretDown}))),c().createElement("ul",{className:"parameter-section-items "+(s?"open":"closed")},Object.entries(n).map((([e,t])=>c().createElement("li",{className:"parameter"},c().createElement(R,{id:e,schema:t,error:a[e],onChange:r})))))))}))`
  .parameter-section-container button {
    width: 100%;
    display: flex;
    padding: 15px 0;
    justify-content: space-between;
    align-items: center;
    border: none;
    outline: none;
    background: transparent;
    cursor: pointer;
  }

  .parameter-section-container button h3 svg {
    margin-right: 15px;
  }

  .parameter-section-container button h3 {
    font-size: 16px;
    font-weight: normal;
    color: #e34040;
  }

  .parameter-section-container.valid button h3 {
    color: black;
  }

  .parameter-section-items {
    transition: 0.2s ease-in-out all;
  }

  .parameter-section-items.closed {
    display: none;
  }

  .parameter-section-items.open {
    padding-top: 15px;
    display: block;
  }
`;const L=m()((({className:e})=>{const t=(0,d.useParams)(),n=(0,d.useNavigate)(),[a,r]=(0,i.useState)(),[o,s]=(0,i.useState)({}),[l,p]=(0,i.useState)(!1),[m,u]=(0,i.useState)({}),[f,g]=(0,i.useState)([]);(0,i.useEffect)((()=>{(async()=>{const e=await(async()=>await b(`workflows/${t.name}`))();r(e),s(e.defaults);const n=(a=e.schema.definitions,Object.values(a).map((e=>{return Object.assign(Object.assign({},e),{properties:(t=e.properties,Object.entries(t).filter((([e,t])=>!t.hidden&&"out_dir"!==e)).reduce(((e,t)=>Object.assign({[t[0]]:t[1]},e)),{}))});var t})).filter((e=>0!==Object.keys(e.properties).length)));var a;g(n)})()}),[]);const h=(e,t,n)=>{if(""!==n)if(["file-path","directory-path","path"].includes(t)){let a;switch(t){case"file-path":a="file";break;case"directory-path":a="directory";break;default:a="path"}x(e,n,a)}else s(Object.assign(Object.assign({},o),{[e]:n}));else{const t=o,n=e,a=(t[n],function(e,t){var n={};for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&t.indexOf(a)<0&&(n[a]=e[a]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var r=0;for(a=Object.getOwnPropertySymbols(e);r<a.length;r++)t.indexOf(a[r])<0&&Object.prototype.propertyIsEnumerable.call(e,a[r])&&(n[a[r]]=e[a[r]])}return n}(t,["symbol"==typeof n?n:n+""]));s(a)}},x=async(e,t,n="file")=>{const a=encodeURIComponent(t),r=await b(`${n}/${a}`,{method:"GET"});if(!r.exists)return u(Object.assign(Object.assign({},m),{[e]:[r.error]})),void p(!1);u(Object.assign(Object.assign({},m),{[e]:[]})),s(Object.assign(Object.assign({},o),{[e]:t}))};return(0,i.useEffect)((()=>{if(a){const{valid:e,errors:t}=function(e,t){const n=new(E())({allErrors:!0,strictSchema:!1,verbose:!0}).compile(t);return{valid:n(e),errors:n.errors}}(o,a.schema);u(e?{}:(e=>{const t={};return e.forEach((e=>{Object.values(e.params).forEach((n=>{t[n]=[...t[n]||[],e.message||""]}))})),t})(t)),p(e)}}),[o]),a?c().createElement("div",{className:`workflow ${e}`},c().createElement("div",{className:"workflow-container"},c().createElement("div",{className:"workflow-section workflow-header"},c().createElement("h1",null,"Workflow: ",t.name),c().createElement("div",{className:"workflow-details"},c().createElement("div",null,a.desc),c().createElement("div",null,"Version ",a.defaults.wfversion))),c().createElement("div",{className:"workflow-section workflow-parameter-sections"},c().createElement("h2",null,"1. Choose parameters"),c().createElement("div",{className:"workflow-section-contents"},c().createElement("ul",null,f.map((e=>{return c().createElement("li",null,c().createElement(_,{title:e.title,description:e.description,fa_icon:e.fa_icon,properties:e.properties,errors:(t=e.properties,n=m,Object.keys(t).reduce(((e,t)=>Object.prototype.hasOwnProperty.call(n,t)?Object.assign(Object.assign({},e),{[t]:n[t]}):e),{})),onChange:h}));var t,n}))))),c().createElement("div",{className:"workflow-section workflow-launch-control"},c().createElement("h2",null,"2. Launch workflow"),c().createElement("div",{className:"workflow-section-contents"},c().createElement("div",{className:"launch-control "+(l?"active":"inactive")},c().createElement("button",{onClick:()=>(async()=>{if(!l)return;const{instance:e}=await b("instances",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({workflow:t.name,params:o})});n(`/instances/${e.id}`)})()},"Run command")))))):c().createElement(c().Fragment,null)}))`
  background-color: #f6f6f6;

  .workflow-container {
    padding: 50px 0 100px 0 !important;
  }

  .workflow-section {
    width: 100%;
    padding: 15px;
    max-width: 1200px;
    margin: 0 auto 25px auto;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .workflow-section > h2 {
    padding-bottom: 15px;
  }

  .workflow-details div {
    color: #333;
    font-weight: normal;
    font-size: 14px;
    padding-bottom: 5px;
  }

  .workflow-parameter-sections .workflow-section-contents > ul > li {
    background-color: #f6f6f6;
    padding: 15px;
    margin: 0 0 15px 0;
    border-radius: 4px;
  }

  .workflow-launch-control .workflow-section-contents {
    padding: 15px;
    border-radius: 4px;
    background-color: #f6f6f6;
  }

  .workflow-launch-control button {
    padding: 15px 25px;
    margin: 0 15px 0 0;
    border: 1px solid lightgray;
    color: lightgray;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }

  .workflow-launch-control .active button {
    border: 1px solid #1d9655;
    color: #1d9655;
  }
  .workflow-launch-control .active button:hover {
    cursor: pointer;
    background-color: #1d9655;
    color: white;
  }
`,I=m()((({title:e,className:t})=>c().createElement("div",{className:`header-title ${t}`},c().createElement("h1",null,e))))`
  padding: 75px 50px 75px 50px;
  display: flex;
  align-items: center;
  flex-direction: column;
  background-color: white;

  h1 {
    padding: 25px 0;
    text-align: center;
  }
`,U=m()((({className:e})=>{const[t,n]=(0,i.useState)([]);return(0,i.useEffect)((()=>{(async()=>{const e=await b("workflows");n(e)})()}),[]),t?c().createElement("div",{className:`workflows-list ${e}`},c().createElement("ul",null,Object.values(t).map((e=>c().createElement("li",null,c().createElement("div",{className:"workflow"},c().createElement("div",null,c().createElement("div",{className:"workflow-header"},c().createElement("span",null,"Version ",e.defaults.wfversion),c().createElement("h3",null,e.name)),c().createElement("div",{className:"workflow-buttons"},c().createElement("a",{className:"workflow-url",href:e.url},"Github"),c().createElement(d.Link,{className:"workflow-link",to:`/workflows/${e.name}`},c().createElement("div",null,"Open workflow")))))))))):c().createElement("div",{className:`workflows-list empty ${e}`},c().createElement("div",{className:"empty"},c().createElement("div",null,"No workflows to display.")))}))`
  max-width: 1200px;
  margin: 50px auto 0 auto;

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .workflow {
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }
  h3 {
    font-size: 24px;
  }

  .workflow span {
    color: #333;
  }

  .workflow-header span {
    text-transform: uppercase;
    font-size: 12px;
    padding-bottom: 5px;
    color: #a0a0a0;
  }
  .workflow-header {
    display: flex;
    justify-content: space-between;
    flex-direction: column-reverse;
  }
  .workflow-buttons {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .workflow-link {
    color: #1d9655;
  }
  .workflow-buttons div {
    padding: 15px 25px;
    border: 1px solid #1d9655;
    color: #1d9655;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
  }
  .workflow-buttons div:hover {
    background-color: #1d9655;
    color: white;
  }
`,$=U,T=m()((({className:e})=>c().createElement("div",{className:`workflows-panel ${e}`},c().createElement(I,{title:"Workflows"}),c().createElement("div",{className:"workflows-panel-section"},c().createElement($,null)))))`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .workflows-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`,D=m()((({className:e,onlyTracked:t})=>{const[n,a]=(0,i.useState)([]),[r,o]=(0,i.useState)([]);(0,i.useEffect)((()=>{(async()=>{const e=await b("instances"),t=Object.values(e),n=t.filter((e=>["LAUNCHED"].includes(e.status)));a(t),o(n)})()}),[]),(0,i.useEffect)((()=>{const e=setInterval((()=>(async()=>{const e=await Promise.all(r.map((async e=>await b(`instances/${e.id}`,{method:"GET",headers:{"Content-Type":"application/json"}}))));o(e)})()),5e3);return()=>{clearInterval(e)}}),[r]);const s=(t?r:n).sort(((e,t)=>e.created_at<t.created_at?1:e.created_at>t.created_at?-1:0));return 0!==s.length?c().createElement("div",{className:`instance-list ${e}`},c().createElement("ul",null,s.map((e=>c().createElement("li",null,c().createElement("div",{className:"instance"},c().createElement("div",null,c().createElement("div",{className:"instance-header"},c().createElement("h2",null,"ID: ",e.id),c().createElement("span",null,e.workflow," | Created: ",e.created_at)),c().createElement("div",{className:"instance-bar"},c().createElement("div",{className:"instance-status"},c().createElement(f,{status:e.status}),c().createElement("p",null,e.status)),c().createElement(d.Link,{className:"instance-link",to:`/instances/${e.id}`},c().createElement("div",null,"View Instance")))))))))):c().createElement("div",{className:`instance-list ${e}`},c().createElement("div",{className:"empty"},c().createElement("div",null,c().createElement("p",null,"No workflows currently running..."),c().createElement(d.Link,{className:"instance-link",to:"/instances"},c().createElement("div",null,"View history")))))}))`
  max-width: 1200px;
  margin: 50px auto 0 auto;

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .empty p {
    padding-bottom: 10px;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }
  .instance {
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }
  h3 {
    font-size: 24px;
  }
  .instance span {
    color: #333;
  }
  .instance-header h2 {
    padding: 5px 0;
  }
  .instance-header span {
    text-transform: uppercase;
    font-size: 12px;
    color: #a0a0a0;
  }
  .instance-header {
    display: flex;
    justify-content: space-between;
    flex-direction: column-reverse;
    padding-bottom: 15px;
  }
  .instance-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .instance-status {
    display: flex;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    align-items: center;
  }
  .instance-status p {
    padding-left: 15px;
  }
  .instance-link {
    color: #005c75;
  }
  .instance-link div {
    padding: 15px 25px;
    border: 1px solid #005c75;
    color: #005c75;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
  }
  .instance-link div:hover {
    background-color: #005c75;
    color: white;
  }
`,A=D,F=m()((({className:e})=>c().createElement("div",{className:`instances-panel ${e}`},c().createElement(I,{title:"History"}),c().createElement("div",{className:"instances-panel-section"},c().createElement(A,null)))))`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .instances-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`,P=m()((({className:e})=>c().createElement("div",{className:`index-panel ${e}`},c().createElement("div",{className:"index-panel-intro"},c().createElement("h1",null,"EPI2ME Labs Workflows (Beta)"),c().createElement("p",null,"EPI2ME Labs maintains a growing collection of workflows covering a range of everyday bioinformatics needs. These are free and open to use by anyone. Browse the list below and get started.")),c().createElement("div",{className:"index-panel-section"},c().createElement("h2",null,"Available workflows"),c().createElement($,null)),c().createElement("div",{className:"index-panel-section"},c().createElement("h2",null,"Tracked instances"),c().createElement(A,{onlyTracked:!0})))))`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .index-panel-intro {
    padding: 75px 50px 75px 50px;
    display: flex;
    align-items: center;
    flex-direction: column;
    background-color: white;
  }

  .index-panel-intro h1 {
    padding: 25px 0;
    text-align: center;
  }

  .index-panel-intro p {
    max-width: 800px;
    text-align: center;
    font-size: 16px;
    line-height: 1.7em;
  }

  .index-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`,M=()=>{const e=new Blob(['\n  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="148" height="198" viewBox="0 0 148 198">\n    <defs>\n      <filter id="Rectangle_1" x="0" y="0" width="148" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n      <filter id="Rectangle_2" x="0" y="130" width="148" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-2"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-2"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n      <filter id="Rectangle_3" x="0" y="65" width="73" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-3"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-3"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n    </defs>\n    <g id="Component_1_2" data-name="Component 1 – 2" transform="translate(9 6)">\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_1)">\n        <rect id="Rectangle_1-2" data-name="Rectangle 1" width="130" height="50" rx="5" transform="translate(9 6)" fill="#08bbb2"/>\n      </g>\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_2)">\n        <rect id="Rectangle_2-2" data-name="Rectangle 2" width="130" height="50" rx="5" transform="translate(9 136)" fill="#0179a4"/>\n      </g>\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_3)">\n        <rect id="Rectangle_3-2" data-name="Rectangle 3" width="55" height="50" rx="5" transform="translate(9 71)" fill="#fccb10"/>\n      </g>\n    </g>\n  </svg>\n'],{type:"image/svg+xml"}),t=URL.createObjectURL(e);return c().createElement("div",{className:"labsLogo"},c().createElement("img",{src:t,alt:"The EPI2ME Labs logo"}))},G=m()((({className:e})=>c().createElement("header",{className:`header ${e}`},c().createElement("div",{className:"header-section left-navigation"},c().createElement(d.Link,{to:"/workflows"},"Workflows"),c().createElement(d.Link,{to:"/instances"},"History")),c().createElement("div",{className:"header-section center-navigation"},c().createElement(d.Link,{to:"/"},c().createElement(M,null))),c().createElement("div",{className:"header-section right-navigation"},c().createElement("a",{href:"https://labs.epi2me.io/"},"Labs Blog")))))`
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  background-color: #00485b;
  color: white;

  .labsLogo img {
    width: 25px;
  }

  .header-section {
    width: calc(100% / 3);
    display: flex;
    align-items: center;
  }

  .left-navigation a {
    padding-right: 25px;
  }

  .center-navigation {
    justify-content: center;
  }

  .right-navigation {
    justify-content: right;
  }

  a {
    font-weight: bold;
  }
`;var B=n(381),V=n.n(B);const W=m()((({className:e})=>c().createElement("footer",{className:`footer ${e}`},c().createElement("p",null,"@2008 - ",V()().year()," Oxford Nanopore Technologies. All rights reserved"))))`
  width: 100%;
  padding: 25px;
  text-align: center;
  box-sizing: border-box;
`,H=m().div``;class q extends o.ReactWidget{constructor(e){super(),this.docTrack=e,this.addClass("jp-ReactWidget"),this.addClass("epi2melabs-wfpage-widget")}render(){return c().createElement(d.MemoryRouter,null,c().createElement(H,null,c().createElement("main",null,c().createElement(G,null),c().createElement("div",null,c().createElement(d.Routes,null,c().createElement(d.Route,{path:"/workflows/:name",element:c().createElement(L,null)}),c().createElement(d.Route,{path:"/workflows",element:c().createElement(T,null)}),c().createElement(d.Route,{path:"/instances/:id",element:c().createElement(x,{docTrack:this.docTrack})}),c().createElement(d.Route,{path:"/instances",element:c().createElement(F,null)}),c().createElement(d.Route,{path:"/",element:c().createElement(P,null)}))),c().createElement(W,null))))}}const J="@epi2melabs/epi2melabs-wfpage:plugin",K="create-epi2me-labs-launcher",Y={id:J,autoStart:!0,requires:[s.ILauncher,a.ISettingRegistry,r.IDocumentManager],activate:(e,t,n,a)=>{const{commands:r,shell:s}=e;Promise.all([e.restored,n.load(J)]).then((([,e])=>{r.addCommand(K,{caption:"Create an EPI2ME Labs workflow launcher",label:"Workflows (Beta)",icon:l,execute:()=>{const e=new q(a),t=new o.MainAreaWidget({content:e});t.title.label="EPI2ME Labs",s.add(t,"main")}}),t&&t.add({command:K,category:"EPI2ME Labs"})}))}}},6700:(e,t,n)=>{var a={"./af":2786,"./af.js":2786,"./ar":867,"./ar-dz":4130,"./ar-dz.js":4130,"./ar-kw":6135,"./ar-kw.js":6135,"./ar-ly":6440,"./ar-ly.js":6440,"./ar-ma":7702,"./ar-ma.js":7702,"./ar-sa":6040,"./ar-sa.js":6040,"./ar-tn":7100,"./ar-tn.js":7100,"./ar.js":867,"./az":1083,"./az.js":1083,"./be":9808,"./be.js":9808,"./bg":8338,"./bg.js":8338,"./bm":7438,"./bm.js":7438,"./bn":8905,"./bn-bd":6225,"./bn-bd.js":6225,"./bn.js":8905,"./bo":1560,"./bo.js":1560,"./br":1278,"./br.js":1278,"./bs":622,"./bs.js":622,"./ca":2468,"./ca.js":2468,"./cs":5822,"./cs.js":5822,"./cv":877,"./cv.js":877,"./cy":7373,"./cy.js":7373,"./da":4780,"./da.js":4780,"./de":9740,"./de-at":217,"./de-at.js":217,"./de-ch":894,"./de-ch.js":894,"./de.js":9740,"./dv":5300,"./dv.js":5300,"./el":837,"./el.js":837,"./en-au":8348,"./en-au.js":8348,"./en-ca":7925,"./en-ca.js":7925,"./en-gb":2243,"./en-gb.js":2243,"./en-ie":6436,"./en-ie.js":6436,"./en-il":7207,"./en-il.js":7207,"./en-in":4175,"./en-in.js":4175,"./en-nz":6319,"./en-nz.js":6319,"./en-sg":1662,"./en-sg.js":1662,"./eo":2915,"./eo.js":2915,"./es":5655,"./es-do":5251,"./es-do.js":5251,"./es-mx":6112,"./es-mx.js":6112,"./es-us":1146,"./es-us.js":1146,"./es.js":5655,"./et":5603,"./et.js":5603,"./eu":7763,"./eu.js":7763,"./fa":6959,"./fa.js":6959,"./fi":1897,"./fi.js":1897,"./fil":2549,"./fil.js":2549,"./fo":4694,"./fo.js":4694,"./fr":4470,"./fr-ca":3049,"./fr-ca.js":3049,"./fr-ch":2330,"./fr-ch.js":2330,"./fr.js":4470,"./fy":5044,"./fy.js":5044,"./ga":9295,"./ga.js":9295,"./gd":2101,"./gd.js":2101,"./gl":8794,"./gl.js":8794,"./gom-deva":7884,"./gom-deva.js":7884,"./gom-latn":3168,"./gom-latn.js":3168,"./gu":5349,"./gu.js":5349,"./he":4206,"./he.js":4206,"./hi":94,"./hi.js":94,"./hr":316,"./hr.js":316,"./hu":2138,"./hu.js":2138,"./hy-am":1423,"./hy-am.js":1423,"./id":9218,"./id.js":9218,"./is":135,"./is.js":135,"./it":626,"./it-ch":150,"./it-ch.js":150,"./it.js":626,"./ja":9183,"./ja.js":9183,"./jv":4286,"./jv.js":4286,"./ka":2105,"./ka.js":2105,"./kk":7772,"./kk.js":7772,"./km":8758,"./km.js":8758,"./kn":9282,"./kn.js":9282,"./ko":6778,"./ko.js":6778,"./ku":1408,"./ku.js":1408,"./ky":3291,"./ky.js":3291,"./lb":6841,"./lb.js":6841,"./lo":5466,"./lo.js":5466,"./lt":7010,"./lt.js":7010,"./lv":7595,"./lv.js":7595,"./me":9861,"./me.js":9861,"./mi":5493,"./mi.js":5493,"./mk":5966,"./mk.js":5966,"./ml":7341,"./ml.js":7341,"./mn":5115,"./mn.js":5115,"./mr":370,"./mr.js":370,"./ms":9847,"./ms-my":1237,"./ms-my.js":1237,"./ms.js":9847,"./mt":2126,"./mt.js":2126,"./my":6165,"./my.js":6165,"./nb":4924,"./nb.js":4924,"./ne":6744,"./ne.js":6744,"./nl":3901,"./nl-be":9814,"./nl-be.js":9814,"./nl.js":3901,"./nn":3877,"./nn.js":3877,"./oc-lnc":2135,"./oc-lnc.js":2135,"./pa-in":5858,"./pa-in.js":5858,"./pl":4495,"./pl.js":4495,"./pt":9520,"./pt-br":7971,"./pt-br.js":7971,"./pt.js":9520,"./ro":6459,"./ro.js":6459,"./ru":1793,"./ru.js":1793,"./sd":950,"./sd.js":950,"./se":490,"./se.js":490,"./si":124,"./si.js":124,"./sk":4249,"./sk.js":4249,"./sl":4985,"./sl.js":4985,"./sq":1104,"./sq.js":1104,"./sr":9131,"./sr-cyrl":9915,"./sr-cyrl.js":9915,"./sr.js":9131,"./ss":5893,"./ss.js":5893,"./sv":8760,"./sv.js":8760,"./sw":1172,"./sw.js":1172,"./ta":7333,"./ta.js":7333,"./te":3110,"./te.js":3110,"./tet":2095,"./tet.js":2095,"./tg":7321,"./tg.js":7321,"./th":9041,"./th.js":9041,"./tk":9005,"./tk.js":9005,"./tl-ph":5768,"./tl-ph.js":5768,"./tlh":9444,"./tlh.js":9444,"./tr":2397,"./tr.js":2397,"./tzl":8254,"./tzl.js":8254,"./tzm":1106,"./tzm-latn":699,"./tzm-latn.js":699,"./tzm.js":1106,"./ug-cn":9288,"./ug-cn.js":9288,"./uk":7691,"./uk.js":7691,"./ur":3795,"./ur.js":3795,"./uz":6791,"./uz-latn":588,"./uz-latn.js":588,"./uz.js":6791,"./vi":5666,"./vi.js":5666,"./x-pseudo":4378,"./x-pseudo.js":4378,"./yo":5805,"./yo.js":5805,"./zh-cn":5057,"./zh-cn.js":5057,"./zh-hk":5726,"./zh-hk.js":5726,"./zh-mo":9807,"./zh-mo.js":9807,"./zh-tw":4152,"./zh-tw.js":4152};function r(e){var t=o(e);return n(t)}function o(e){if(!n.o(a,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return a[e]}r.keys=function(){return Object.keys(a)},r.resolve=o,e.exports=r,r.id=6700}}]);