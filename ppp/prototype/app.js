'use strict';

// Deliberately fictional catalogue for design review. No network or persistent storage.
const products = [
  {id:'ellipse',name:'Ellipse Hoops',material:'Gold-plated silver',price:4800,image:'hoops.svg',type:'silver',festive:true,label:'THE EVERYDAY EDIT',collection:'Everyday / gold-plated silver',stock:'Ready-stock example — availability not verified',buyable:true,description:'An easy, sculptural curve with a warm gold finish. A sample direction for everyday pieces that move naturally between work, weekends and occasions.',weight:'Supplier specification pending',purity:'Silver purity and plating specification pending',size:'Dimensions to be confirmed'},
  {id:'pebble',name:'Pebble Pendant',material:'18K gold',price:11800,image:'studs.svg',type:'gold',festive:false,label:'SMALL GOLD',collection:'Small Gold / 18K',stock:'Supplier confirmation example — request details first',buyable:false,description:'A small, organic form with a personal feel. This concept illustrates the lightweight real-gold collection; the actual design, price and weight require supplier confirmation.',weight:'Approx. 1 g collection intention; actual weight pending',purity:'18K concept; supplier documentation pending',size:'Pendant dimensions and chain inclusion pending'},
  {id:'lilt',name:'Lilt Ring',material:'Gold-plated silver',price:3200,image:'ring.svg',type:'silver',festive:false,label:'THE EVERYDAY EDIT',collection:'Everyday / gold-plated silver',stock:'Ready-stock example — availability not verified',buyable:true,description:'A gently curved band, understated on its own and expressive with the pieces you already wear. Shown as a design concept; sizing will follow the selected catalogue.',weight:'Supplier specification pending',purity:'Silver purity and plating specification pending',size:'Sample size only; live ring sizes to be supplied'},
  {id:'petal',name:'Petal Pendant',material:'22K gold',price:17500,image:'pendant.svg',type:'gold',festive:true,label:'A FESTIVE NOTE',collection:'Festive / Small Gold / 22K',stock:'Made-to-order example — quote and lead time required',buyable:false,description:'A softly fluted form for moments worth dressing for. A sample 22K direction, with final metal weight, chain inclusion and making charges to be confirmed.',weight:'Actual net gold weight pending',purity:'22K concept; supplier documentation pending',size:'Dimensions and chain inclusion to be confirmed'}
];
const money = value => new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format(value);
const $ = selector => document.querySelector(selector);
let activeFilter = 'all';
let currentProduct = products[0];
const bag = new Map();
let toastTimer;

function card(product) {
  return `<article class="product-card"><a href="#product/${product.id}"><div class="card-image"><img src="assets/${product.image}" alt="Concept illustration of ${product.name.toLowerCase()}" width="600" height="750" loading="lazy"><span class="card-label">${product.label}</span><span class="card-arrow" aria-hidden="true"><svg class="arrow" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16 16 4M5 4h11v11" fill="none" stroke="currentColor" stroke-width="1.2"/></svg></span></div><div class="card-info"><p class="card-type">${product.material}</p><h3>${product.name}</h3><p class="card-price">${money(product.price)}</p></div></a></article>`;
}
function renderCollection() {
  const selection=products.filter(product => activeFilter==='all' || (activeFilter==='festive' ? product.festive : product.type===activeFilter));
  $('#product-grid').innerHTML=selection.map(card).join('');
  $('#result-count').textContent=`${selection.length} ${selection.length===1?'piece':'pieces'}`;
  document.querySelectorAll('[data-filter]').forEach(button => {
    const active=button.dataset.filter===activeFilter;
    button.classList.toggle('active',active);
    button.setAttribute('aria-pressed',String(active));
  });
}
function renderProduct(product) {
  currentProduct=product;
  $('#product-title').textContent=product.name;
  $('#breadcrumb-name').textContent=product.name;
  $('#detail-collection').textContent=product.collection;
  $('#detail-material').textContent=product.material;
  $('#detail-price').textContent=money(product.price);
  $('#detail-description').textContent=product.description;
  $('#detail-stock').textContent=product.stock;
  $('#detail-image').src=`assets/${product.image}`;
  $('#detail-image').alt=`Concept illustration of ${product.name.toLowerCase()}; not a photograph of a product for sale`;
  $('#detail-specs').innerHTML=`<dt>Material</dt><dd>${product.material}</dd><dt>Purity / finish</dt><dd>${product.purity}</dd><dt>Weight</dt><dd>${product.weight}</dd><dt>Size</dt><dd>${product.size}</dd>`;
  $('#product-action').innerHTML=product.buyable?'Add to preview bag <span aria-hidden="true"><svg class="arrow" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16 16 4M5 4h11v11" fill="none" stroke="currentColor" stroke-width="1.2"/></svg></span>':'Request piece details <span aria-hidden="true"><svg class="arrow" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 16 16 4M5 4h11v11" fill="none" stroke="currentColor" stroke-width="1.2"/></svg></span>';
  $('#quantity').value='1';
  $('#quantity').disabled=!product.buyable;
}
function route() {
  const hash=window.location.hash;
  const isProduct=hash.startsWith('#product/');
  const product=isProduct ? products.find(item=>`#product/${item.id}`===hash) : null;
  $('#view-home').hidden=Boolean(product);
  $('#view-product').hidden=!product;
  if(product){
    renderProduct(product);
    document.title=`${product.name} — The Edit design concept`;
    window.scrollTo({top:0,behavior:'instant'});
    $('#main').focus({preventScroll:true});
  }else{
    document.title='The Edit — jewellery concept';
    if(isProduct){window.location.replace('#home');return;}
    requestAnimationFrame(()=>{
      if(['#collection','#appointments','#story'].includes(hash)) $(hash).scrollIntoView({behavior:'instant'});
      else window.scrollTo({top:0,behavior:'instant'});
    });
  }
}
function openDialog(id) {
  document.querySelectorAll('dialog[open]').forEach(dialog=>dialog.close());
  $(id).showModal();
}
function toast(message) {
  clearTimeout(toastTimer);
  $('#toast').textContent=message;
  $('#toast').classList.add('visible');
  toastTimer=setTimeout(()=>$('#toast').classList.remove('visible'),3200);
}
function renderBag() {
  let total=0,count=0;
  const rows=[];
  bag.forEach((quantity,id)=>{
    const product=products.find(item=>item.id===id);
    total+=quantity*product.price;count+=quantity;
    rows.push(`<div class="bag-item"><img src="assets/${product.image}" alt="Concept illustration of ${product.name}" width="70" height="85"><div><h3>${product.name}</h3><p>${product.material}</p><p>Quantity ${quantity} · ${money(product.price*quantity)}</p></div><button class="remove-item" data-remove="${id}" aria-label="Remove ${product.name} from preview bag">Remove</button></div>`);
  });
  $('#bag-items').innerHTML=rows.length?rows.join(''):'<p class="empty-state">Your preview bag is empty. Explore a ready-stock example to try adding a piece.</p>';
  $('#bag-summary').innerHTML=count?`<p class="bag-total"><span>Illustrative subtotal</span><strong>${money(total)}</strong></p><p class="small-note">This is not a payable total. There is no checkout in the design preview.</p>`:'';
  $('#bag-count').textContent=String(count);
  $('#bag-open').setAttribute('aria-label',`Open preview bag, ${count} ${count===1?'item':'items'}`);
}
function showAssistance() {
  $('#info-title').textContent=`About ${currentProduct.name}.`;
  $('#info-body').innerHTML='<p>The live site will offer customer-initiated WhatsApp assistance with the selected product reference. The team can confirm availability, specifications, price and lead time before taking payment.</p><p>This preview has no business phone number or messaging connection. No message has been sent.</p>';
  openDialog('#info-dialog');
}
function renderSearch() {
  const query=$('#search-input').value.trim().toLowerCase();
  const matches=products.filter(product=>`${product.name} ${product.material} ${product.collection}`.toLowerCase().includes(query));
  $('#search-results').innerHTML=matches.length?matches.map(product=>`<a class="search-result" href="#product/${product.id}"><img src="assets/${product.image}" alt="" width="65" height="75"><span><strong>${product.name}</strong><small>${product.material} · ${money(product.price)} · illustrative price</small></span></a>`).join(''):'<p class="empty-state">No sample pieces match. Try “gold”, “silver” or “ring”.</p>';
}
const information={
  story:{title:'Rooted in jewellery.',body:'<p>The founder’s parent business is an established jewellery retailer in Erode, with existing supplier relationships and sourcing experience. The new brand introduces a deliberately limited, curated selection for online customers.</p><p>The parent brand will be introduced here, in Our Story. Its name, verified history and approved narrative are still being prepared. The working wordmark “THE EDIT” is not a final brand name.</p>'},
  care:{title:'Know your piece.',body:'<p>Gold-plated silver, 18K gold and 22K gold will have distinct, supplier-backed material and care information. Every published product must identify its actual material, relevant purity, weight and finish.</p><p>Care, warranty and documentation will be specific to each selected product. This design concept does not claim that its sample items are hallmarked, waterproof or covered by a warranty.</p>'},
  delivery:{title:'Delivery & aftercare.',body:'<p>The proposed store will offer online payments without COD. Delivery eligibility and charges will depend on the selected insured jewellery carrier. The free-delivery threshold is not yet set.</p><p>The intended return journey is request, eligibility review, authorised return, receipt and inspection, then a communicated refund decision. Exact eligibility, timelines and consumer-law review remain launch requirements.</p><p>No shipping or return service is connected to this preview.</p>'},
  contact:{title:'Here to help.',body:'<p>Live business contact details and support hours will be added after approval. Consultation handling will be coordinated through the parent-company team and suppliers.</p><p>This offline concept does not use analytics, send form data or connect to WhatsApp. The demonstration bag stays in memory only. Example appointment entries are discarded after the local form demonstration. A production privacy notice and retention process remain to be defined.</p>'}
};
document.addEventListener('click',event=>{
  const close=event.target.closest('[data-close]');
  if(close){close.closest('dialog').close();return;}
  const filter=event.target.closest('[data-filter]');
  if(filter){activeFilter=filter.dataset.filter;renderCollection();return;}
  const shop=event.target.closest('[data-shop]');
  if(shop){activeFilter=shop.dataset.shop;renderCollection();}
  const anchor=event.target.closest('dialog a[href^="#"]');
  if(anchor)anchor.closest('dialog').close();
  const remove=event.target.closest('[data-remove]');
  if(remove){bag.delete(remove.dataset.remove);renderBag();$('#bag-dialog .close-button').focus();return;}
  if(event.target.closest('[data-appointment]')){
    $('#appointment-form').reset();$('#appointment-form').hidden=false;$('#appointment-result').hidden=true;openDialog('#appointment-dialog');return;
  }
  const info=event.target.closest('[data-info]');
  if(info){const item=information[info.dataset.info];$('#info-title').textContent=item.title;$('#info-body').innerHTML=item.body;openDialog('#info-dialog');}
});
$('#search-open').addEventListener('click',()=>{$('#search-input').value='';renderSearch();openDialog('#search-dialog');$('#search-input').focus();});
$('#search-input').addEventListener('input',renderSearch);
$('#bag-open').addEventListener('click',()=>{renderBag();openDialog('#bag-dialog');});
$('#menu-open').addEventListener('click',()=>openDialog('#menu-dialog'));
$('#product-assistance').addEventListener('click',showAssistance);
$('#product-action').addEventListener('click',()=>{
  if(!currentProduct.buyable){showAssistance();return;}
  const quantity=Number($('#quantity').value);
  const next=(bag.get(currentProduct.id)||0)+quantity;
  if(next>9){toast('The preview supports up to 9 of one sample piece.');return;}
  bag.set(currentProduct.id,next);renderBag();openDialog('#bag-dialog');
});
$('#appointment-form').addEventListener('submit',event=>{
  event.preventDefault();
  $('#appointment-form').reset();$('#appointment-form').hidden=true;$('#appointment-result').hidden=false;
  $('#appointment-result button').focus();
});
document.querySelectorAll('dialog').forEach(dialog=>{
  dialog.addEventListener('click',event=>{
    if(event.target!==dialog)return;
    const bounds=dialog.getBoundingClientRect();
    if(event.clientX<bounds.left||event.clientX>bounds.right||event.clientY<bounds.top||event.clientY>bounds.bottom)dialog.close();
  });
  dialog.addEventListener('close',()=>{
    if(dialog.id==='appointment-dialog')$('#appointment-form').reset();
  });
});
// Search fields consume Escape to clear text in some browsers. Keep modal
// dismissal consistent with the visible close control, including that case.
document.addEventListener('keydown',event=>{
  if(event.key!=='Escape')return;
  const dialog=document.querySelector('dialog[open]');
  if(dialog){event.preventDefault();event.stopPropagation();dialog.close();}
},true);
window.addEventListener('hashchange',route);
renderCollection();renderBag();route();
