const data = document.currentScript.dataset
const user = data.user
const buttonAdd = data.buttonadd
const main = data.main
const divitems = data.divitems
const fields = JSON.parse(data.fields.replace(/'/g, '"'))

// (function() {
//   // Chama o método pra numerar os objetos ao carregar a página.
//   reorderItems()
// })();

document.querySelector(buttonAdd).addEventListener('click', function() {
  setTimeout(() => {
    reorderItems()
  }, 500)
})

function reorderItems() {
  Array.from(document.querySelectorAll("[id^='item-']"))
    .forEach((item, i) => {
      item.setAttribute('id', 'item-' + i)

      if (!item.querySelector('[data-field="' + main + '"]')) {
        return
      }

      fields.forEach((field) => {
        item.querySelector('[data-field="' + field + '"]').setAttribute('name', 'items-' + i + '-' + field)
        item.querySelector('[data-field="' + field + '"]').setAttribute('id', 'id_items-' + i + '-' + field)
        if (field == 'product') {
          item.querySelector('[data-field="' + field + '"]').setAttribute('hx-get', '/ecommerce/product/price/')
          item.querySelector('[data-field="' + field + '"]').setAttribute('hx-target', '#id_items-'+ i + '-price')
          item.querySelector('[data-field="' + field + '"]').setAttribute('hx-swap', 'outerHTML')
        }
      })
  })

  Array.from(document.querySelectorAll("#id_id"))
    .forEach((item, i) => item.setAttribute('name', 'items-' + (i + 1) + '-id'))

  let totalItems = document.getElementById(divitems).querySelectorAll("[id^='item-']").length
  document.querySelector('#id_items-TOTAL_FORMS').value = totalItems

  // htmx.org/api/#process
  htmx.process(document.getElementById(divitems))
}

function removeRow() {
  const span = event.target.parentNode
  const div = span.parentNode
  div.parentNode.removeChild(div)

  reorderItems()
}

Array.from(document.querySelectorAll('.remove-row'))
  .forEach((item, i) => {
    item.addEventListener('click', function() {
      document.querySelector('button[type="submit"]').style.display = 'none'
      document.querySelector('#btn-close').style.display = 'block'
    })
  })
