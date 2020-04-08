# Movie Reviews

> A simple movie review app with Django

<br>

<br>

### 진행하며 어려웠던 점 & 새롭게 알게된 점

- #### `truncatechars_html`

  - 전체 review list를 보여주는 page( `review_html` ) 에서는 **content**를 다 보여주지 않고 **ellipsis** 로 표현하고 싶어서 Django documentation을 찾아보았더니 역시나 **built-in template**이 있었다...!

    ex)

    ```html
    {{review.content|truncatechars_html:30}}
    ```

  - 이렇게 해서 30자만 보여주어서 list에서는 각 review에 대한 크기가 일정하게 유지하도록 구현했다.

- #### `linebreaksbr`

  - Django는 좋은 template을 많이 갖고 있는 것 같다.  `\n` 을    `<br>` 로 바꿔주어 `<input>`에 입력된 줄바꿈을 출력 시 적용되도록 구현했다.

    ex)

    ```html
    {{review.content|linebreaksbr}}
    ```

- #### `.raw()`

  - Django에서는 **SQL query**를 어떻게 작성할지 궁금해서 찾아보니 `.raw`라는 method가 있었다

  - *Raw query must include the primary key* 라고 error가 나서 찾아보고 select문에 `rowid as id` 를 추가하여 해결했다

  - Django에서 SQL문을 쓸 때 table명에 `[app name]_table name`인 것을 새로 알게 되었다  

    ex)

    ```python
    Review.objects.raw('select rowid as id, movie_title, avg_rate from (select movie_title, avg(rank) as avg_rate from community_review group by movie_title order by avg_rate desc) LIMIT 3')
    ```

    

<br>

<br>

### Features

- #### `Search`

  - 영화 제목을 기준으로 검색하도록 `Review.objects.filter(movie_title__icontains=keyword)` 를 활용했다.

- #### `Top rated movies`

  - 평점이 가장 높은 3개의 영화를 리뷰 리스트 화면 상단에 출력하는 기능을 추가했다.

  - 글이 하나도 없을 때에는 Top rated movie가 출력될 `table`을 출력하지 않기 위해 조건문을 사용했다. 

    ( `views.py`에서 **ranks**로 순위 정보를 넘겨준다)

    ```html
    {% if ranks %}
     ...
    {% endif %}
    ```

    

<br>

<br>

###  Deployment

- `MS Azure` 에 `Fabric` 으로 배포했다!
  - 처음 **Azure** 써보면서 많이 헤맸다. 
  - `Azure Virtual Machine` 만들고 배포한 과정을 **Github TIL repo**에 정리해서 올려야겠다.
  - Deployed in [HERE](https://bit.ly/Movie-reviews) !





<br>

<br>

### 더 추가할 기능

- [x] Order by `rank`
  - 아무래도 review site인 만큼 영화 평점순으로 정렬하면 좋을 것 같다! <s> 추가해야징</s>
  - 추가했다!

- [x] Deployment
  - 지난 프로젝트에서 `PythonAnywhere`에 배포 해봤으므로 이번엔 다른 web hosting site에 배포해봐야겠다!
  - `MS Azure` 에 배포했다!
