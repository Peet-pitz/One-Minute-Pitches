from flask import render_template,redirect,url_for,request
from . import main
from flask_login import login_required,login_user,logout_user
from ..models import Pitch,Comments
from .forms import PitchForm,CommentForm
from ..import db

@main.route('/')
def index():
    title = 'Home'

    pitches = Pitch.get_pitches()
    comments=Comments.get_comments()

    return render_template('index.html' ,title=title, pitches=pitches,comments=comments)

@main.route('/pitch/new',methods=['GET','POST'])
@login_required
def new_pitch():
    form= PitchForm()
    if form.validate_on_submit():
        title=form.title.data
        description=form.description.data
        like=0
        dislike=0
        new_pitch=Pitch(title=title,description=description,like=like,dislike=dislike)
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title= 'Pitches'
    return render_template('new_pitch.html',pitch_form=form)

@main.route('/comment/new/', methods=['GET','POST'])
@login_required
def new_comment():

    '''
    View new comment route function that returns a page with a form to create a pitch for the specified category
    '''
    comments = Comments.query.all()
    form =CommentForm()
    if form.validate_on_submit():
        name=form.name.data
        new_comment=Comments(name=name)
        new_comment.save_comment()

        return redirect(url_for('.index'))

    title = "New Comment"
    return render_template('new_comment.html', title=title, form=form,comments=comments)

@main.route('/pitch_review/<int:id>',methods=['GET','POST'])

def pitch_review(id):
    pitches=Pitch.query.get_or_404(id)
    if request.args.get("like"):
        pitches.like = pitches.like+1

        db.session.add(pitches)
        db.session.commit()

        return redirect("/pitch_review/{pitch_id}".format(pitch_id=pitches.id))

    elif request.args.get("dislike"):
        pitches.dislike=pitches.dislike+1

        db.session.add(pitches)
        db.session.commit()

        return redirect("/pitch_review/{pitch_id}".format(pitch_id=pitches.id))

    title= 'Pitches'
    return render_template('pitch_review.html',pitches=pitches)
