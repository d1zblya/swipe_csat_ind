from __main__ import app
from flask import render_template, redirect
import aiohttp

@app.route('/reviews/', defaults={'item_id': 'all'}, methods=['GET', 'POST'])
@app.route('/reviews/<item_id>', methods=['GET', 'POST'])
async def reviews_page(item_id):
    """Обработка страницы отзывов"""
    session = aiohttp.ClientSession()
    request_stars_rating = await session.get(f'http://127.0.0.1:5000/api/rating/count/{item_id}')
    stars = await request_stars_rating.json()
    
    request_reviews = await session.get(f'http://127.0.0.1:5000/api/page/review/{item_id}')
    reviews_list = await request_reviews.json()
    
    item = reviews_list['item_info']
    reviews = reviews_list['all_reviews']
    
    item['reviews_rating'] = stars
    
    return render_template(
        'reviews.html',
        reviews=reviews,
        item=item
    )