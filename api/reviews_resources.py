from flask_restful import Resource
from data import db_session
from data.feedback import Feedback
from data.user import User
from flask import jsonify, Response, request
import dataclasses
import json

def parse_criterions(string_lst):
    result = []
    for string in string_lst:
        criterions_dict = {}
        pairs = string.split(';')
        for pair in pairs:
            key, value = pair.split('-')
            criterions_dict[key] = value
        result.append(criterions_dict)
    return result


@dataclasses.dataclass
class CommonReview(Resource):
    def get(self):
        db_sess = db_session.create_session()
        all_rewiews = db_sess.query(User, Feedback).join(User, Feedback.user_id == User.id).all()
        rewiews = [
            {
                'username': user.name,
                'evaluation': rew.evaluation,
                'date': rew.date_of_creation,
                'text': rew.text_feedback
            }
            for user, rew in all_rewiews
        ]
        res = json.dumps(
            {
                'all_rewiews': rewiews
            },
            ensure_ascii=False         
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
    def post(self):
        db_sess = db_session.create_session()
        info = request.json()
        print(info)
        new_review = Feedback(
            
        )
        
        db_sess.add(new_review)
        db_sess.commit()
        db_sess.close()
        
@dataclasses.dataclass
class DetailReview(Resource):
    def get(self, review_id):
        db_sess = db_session.create_session()
        review_request = db_sess.query(User, Feedback).join(User, Feedback.user_id == User.id).filter(Feedback.id == review_id).first()
        if review_request is None:
            return jsonify({'error': 'Not found'}), 404
        user, rew = review_request
        review = [
            {
                'username': user.name,
                'evaluation': rew.evaluation,
                'date': rew.date_of_creation,
                'text': rew.text_feedback
            }
        ]
        res = json.dumps(
            {
                'review': review
            },
            ensure_ascii=False        
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
    
    def put(self, review_id):
        pass
    
    def delete(self, review_id):
        pass
    
@dataclasses.dataclass
class GetUserReviews(Resource):
    def get(self, current_user_id):
        db_sess = db_session.create_session()
        user_reviews_request = db_sess.query(Feedback).filter(Feedback.user_id == current_user_id).all()
        intermediate_result = [info.criterions for info in user_reviews_request]
        result = parse_criterions(intermediate_result)
        user_reviews = [
            {
                'evaluation': int(info.evaluation),
                'date': info.date_of_creation,
                'criterion': crit,
                'advantage': info.advantage,
                'disadvantage': info.disadvantage,
                'text': info.text_feedback
            }
            for info, crit in zip(user_reviews_request, result)
        ]
        res = json.dumps(
            {
                'user_reviews': user_reviews
            },
            ensure_ascii=False    
        )
        db_sess.close()
        return Response(res, content_type='application/json; charset=utf-8')
