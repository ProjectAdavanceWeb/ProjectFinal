const List = document.getElementById('ongrid')
const btnSearch = document.getElementById('btn-search')
// const mealDetailsContent = document.querySelector('.modal-header')
const mealDetailsContent = document.querySelector('.modal-header');


btnSearch.addEventListener('click', getMealList);
List.addEventListener('click', getMealRecipe);

getMealList();


function getMealList() {
    let searchInput = document.getElementById('search-input').value.trim();
    console.log("Input", searchInput);
    fetch(`https://www.themealdb.com/api/json/v1/1/filter.php?i=${searchInput}`)
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            let html = "";
            if (data.meals) {
                data.meals.forEach(meal => {
                    // console.log(meal);
                    html += `
                    <div class="card"  data-id="${meal.idMeal}"">
                        <img src="${meal.strMealThumb}" class="card-img-top imageborder" alt="..." style="width: 100%;">
                        <div class="card-body" style="padding-bottom: 2rem;">
                        <h2 class="card-title">${meal.strMeal}</h2>
                        <a href="#" class="btn btn-primary btn_border recipe-btn" data-toggle="modal" data-target="#DesModal">Go somewhere
                            <br></a>
                        </div>
                    </div>
                `;
                });
                List.classList.remove('notFound')
            } else {
                html = "Sorray, we didn't find any meal!";
                List.classList.add('notFound')
            }
            List.innerHTML = html;
        })
}

function getMealRecipe(e) {
    console.log('GetMealRecipe');
    e.preventDefault();
    if (e.target.classList.contains('recipe-btn')) {
        let mealItem = e.target.parentElement.parentElement;
        console.log(mealItem);
        fetch(`https://www.themealdb.com/api/json/v1/1/lookup.php?i=${mealItem.dataset.id}`)
            .then(response => response.json())
            .then(data => mealRecipeModal(data.meals));
    }
}

function mealRecipeModal(meal) {
    console.log(meal);
    meal = meal[0];
    let html = `
        <h2 class="modal-title text-center"><strong>${meal.strMeal}</strong></h2>
        <br>
        <h4 class="text-center"><kbd>${meal.strCategory}</kbd></h4>
      <div class="modal-body">
        <h3 class="text-center"><Strong>Instructions:</Strong></h3>
        <br>
        <h4 class="text-center">
            ${meal.strInstructions}
        </h4>
      </div>
      <div class="modal-footer">
        <h1 class="text-center"><strong><a href="${meal.strYoutube}">Watch Video</a></strong></h1>
      </div>
    </div>
    `;
    mealDetailsContent.innerHTML = html;

}