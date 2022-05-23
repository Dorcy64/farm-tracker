# Garden Tracking

![alt text](https://imagedelivery.net/hnHx9kxJyligwC1X9CPssg/ca5a85f6-63a3-4af9-1964-9427bae65d00/public)

### Intro

I had an idea of developing an api to track gardening progress, results with grids, labeled as beds. 
First you need to enter all the plants you plan to plant, and the necessary data if not included already.

### Database Design
The databases are going to have the following specification:

```sql
__tablename__ = current_plants
plant_id
planted_on
status [planted/harvested]
harvest_start_date
harvest_end_date
Notes
```


```sql
__tablename__ = plants
Name
Type [Veggies/Fruit, Herbs, Flowers]
good_combos
bad_combos
days_to_harvest
harvest_duration
```

Bed table: This needs to have many relationships.
Since, once the seed status changes we need to free up the bed.

```sql
__tablename__ = beds
bed_id grid_id
bed_type raised/field/container
current_plant relationship
```


## Running

These APIs don't require any api keys since they are intended for development only and not production. If you want to skip all these steps just install [pycharm]("https://www.jetbrains.com/pycharm/") and open this directory in pycharm.

Use pip3 to install all the required dependencies on Mac or Linux.
```sh
python -m pip install --upgrade pip
pip3 install -r requirements.txt
```

Run the flask app on your machine.
```sh
export FLASK_APP=app
flask run
```

## Routes
![alt text](https://imagedelivery.net/hnHx9kxJyligwC1X9CPssg/1390a991-06ef-4be8-a550-a8f9a2846500/public)

### Bed Routes
```http
POST, GET /view-all-beds
```

```http
POST, GET /view-bed/<bed_id>
```
Make sure to include the bed id in the url otherwise you will get a 404 error.

```http
POST /create-bed
```

| Parameter         | Type      | Description                                                                    |
|:------------------|:----------|:-------------------------------------------------------------------------------|
| `bed_id`          | `integer` | **Required**. The new bed's grid id                                            |
| `bed_type`        | `string`  | **Optional**. Can either be field, raised, or container, default is field      |

```http
POST /edit-bed
```

| Parameter         | Type      | Description                                                                   |
|:------------------|:----------|:------------------------------------------------------------------------------|
| `bed_id`          | `integer` | **Required**. The bed's grid id                                               |
| `bed_type`        | `string`  | **Optional**. Can either be field, raised, or container, default is field     |


```http
POST /delete-bed
```

```http
POST /clear-bed
```

| Parameter         | Type      | Description                                                                   |
|:------------------|:----------|:------------------------------------------------------------------------------|
| `bed_id`          | `integer` | **Required**. The bed's grid id                                               |

### Plant Routes

```http
POST, GET /view-all-plants
```

```http
POST /create-plant
```

| Parameter         | Type      | Description                                                                    |
|:------------------|:----------|:-------------------------------------------------------------------------------|
| `title`           | `string`  | **Required**. The new plant's name                                             |
| `days_to_grow`    | `integer` | **Required**. The number of days it takes to grow the plant                    |
| `days_to_harvest` | `integer` | **Required**. The number of days it takes to harvest                           |
| `plant_type`      | `string`  | **Optional**. Plant type either veggie, fruit, Herb, or flower, default=veggie |
| `good_combos`     | `string`  | **Optional**. Comma separated values of suggested nearby plants                |
| `bad_combos`      | `string`  | **Optional**. Comma separated values of plants to avoid planting close by      |


```http
POST /edit-plant
```

| Parameter         | Type      | Description                                                                    |
|:------------------|:----------|:-------------------------------------------------------------------------------|
| `plant_id`        | `integer` | **Required**. The name of the plant to edit                                    |
| `title`           | `string`  | **Required**. The new plant's name                                             |
| `days_to_grow`    | `integer` | **Required**. The number of days it takes to grow the plant                    |
| `days_to_harvest` | `integer` | **Required**. The number of days it takes to harvest                           |
| `plant_type`      | `string`  | **Optional**. Plant type either veggie, fruit, Herb, or flower, default=veggie |
| `good_combos`     | `string`  | **Optional**. Comma separated values of suggested nearby plants                |
| `bad_combos`      | `string`  | **Optional**. Comma separated values of plants to avoid planting close by      |


```http
POST /delete-plant
```

| Parameter         | Type      | Description                                          |
|:------------------|:----------|:-----------------------------------------------------|
| `plant_id`        | `integer` | **Required**. The id of the plant you want to delete |


### Planting Routes

```http
POST /plant-bed
```

| Parameter  | Type      | Description                                                                    |
|:-----------|:----------|:-------------------------------------------------------------------------------|
| `bed_id`   | `integer` | **Required**. The id of the bed you want to plant on                           |
| `plant_id` | `integer` | **Required**. The id of the plant you want to plant on this bed                |
| `notes`    | `string`  | **Optional**. If you want to add a note on this plant plant this is the moment |

```http
POST /edit-bed
```

| Parameter          | Type      | Description                                                                    |
|:-------------------|:----------|:-------------------------------------------------------------------------------|
| `bed_id`           | `integer` | **Required**. The id of the bed you want to plant on                           |
| `plant_id`         | `integer` | **Optional**. The id of the plant you want to plant on this bed                |
| `notes`            | `string`  | **Optional**. If you want to add a note on this plant plant this is the moment |
| `days_ago_planted` | `integer` | **Optional**. How many days ago did you plant this                             |


```http
POST /current-plant-status
```

| Parameter             | Type      | Description                                                                    |
|:----------------------|:----------|:-------------------------------------------------------------------------------|
| `current_plant_id`    | `integer` | **Required**. The id of the current plant you want to change status            |
| `change_plant_status` | `bool`    | **Optional**. true or false if you want to change the plantation's status      |


```http
POST /delete-current-plant
```

| Parameter          | Type      | Description                                                                              |
|:-------------------|:----------|:-----------------------------------------------------------------------------------------|
| `current_plant_id` | `integer` | **Required**. The id of the plantation you want to delete or use clear bed in Bed Routes |


## Responses

Many API endpoints return the JSON representation of the resources created or edited. If a valid request is submitted to retrieve all beds, this will return a JSON response in the following format:

```javascript
[
    {
        "bed_id": 1,
        "bed_type": "raised",
        "current_plant_id": 2,
        "harvest_date": "Thu, 21 Jul 2022 23:14:51 GMT",
        "notes": "Can't wait to get started on this garden",
        "plant_id": "1",
        "plant_name": "Bell Peppers",
        "planted_date": "Sun, 22 May 2022 23:14:51 GMT",
        "status": "planted"
    }
]
```

If you submit a valid request of adding a new plant to the catalog of plants, the api will return the following.

```javascript
{
    "bad_combos": "beans, apricot tree",
    "days_to_grow": 60,
    "days_to_harvest": 60,
    "good_combos": "basil, parsley, onions, spinach, tomatoes, carrots",
    "id": 1,
    "title": "Bell Peppers",
    "type": "veggie"
}
```


## Status Codes

This API returns the following status codes:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |







