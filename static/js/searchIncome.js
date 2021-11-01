const searchSelect =  document.querySelector("#search_income");
const expenses_row =  document.querySelector("#income-rows");

    searchSelect.addEventListener("keyup", e => {
      const searchVal = e.target.value;
      expenses_row.innerHTML = '<h6 class="text-center pt-5">Loading</h6>';
      if (searchVal.length >= 0){
        fetch("/income/search-income/",{
          body: JSON.stringify({searchText: searchVal}),
          method: "POST" 
        }).
        then(res => res.json()).
        then(data => {
          console.log(data);
          if (data.length > 0) {
            expenses_row.innerHTML = '';
            data.forEach(el => {
                const create_row = document.createElement('tr')
                create_row.innerHTML = `
                    <th>${el.amount}</th>
                    <td>${el.description}</td>
                    <td>${el.category}</td>
                    <td>${el.date}</td>
                    <td><a href="${location.href}edit-income/${el.id}" class="btn btn-warning btn-sm">Edit</a></td>
                `
                expenses_row.appendChild(create_row)
            });
          } else {
            expenses_row.innerHTML = `<h4 class="text-center pt-5">No date found!</h4>`
          }
        })
    }
})