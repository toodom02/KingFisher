from flask import render_template, Blueprint, url_for, flash, redirect, request
from flask_login import login_required
from flasksite.main.forms import ContentForm, OpenTimesForm

from flasksite.models import Post


main = Blueprint('main', __name__)


@main.route("/")
def home():
    with open("flasksite/templates/markdown/sub.md", "r", encoding="utf8") as f:
        sub=f.read()
    with open("flasksite/templates/markdown/about.md", "r", encoding="utf8") as f:
        about=f.read()
    with open("flasksite/templates/markdown/contact.md", "r", encoding="utf8") as f:
        contact=f.read()
    with open("flasksite/templates/markdown/opentimes.md", "r", encoding="utf8") as f:
        opentimes=f.read()
    with open("flasksite/templates/markdown/phoneno.md", "r", encoding="utf8") as f:
        phoneno=f.read()
    with open("flasksite/templates/markdown/address.md", "r", encoding="utf8") as f:
        address=f.read()
    with open("flasksite/templates/markdown/email.md", "r", encoding="utf8") as f:
        email=f.read()
    posts = Post.query.order_by(Post.date.desc()).limit(2)
    return render_template('home.html', sub=sub, about=about, opentimes=opentimes, contact=contact, phoneno=phoneno, address=address, email=email, posts=posts)


@main.route("/edit/<mkdwn>", methods=['GET', 'POST'])
@login_required
def edit_text(mkdwn):
    form = ContentForm()
    if form.validate_on_submit():
        if mkdwn == 'address.md':
            content = form.content.data.replace("\r", "")
        else:
            content = form.content.data.replace("\n\n\n", "\n")
        with open(f"flasksite/templates/markdown/{mkdwn}", "w", encoding="utf8") as f:
            f.write(content)
        flash('Content updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        with open(f"flasksite/templates/markdown/{mkdwn}", "r", encoding="utf8") as f:
            content = f.read()
        form.content.data = content.replace("\n\n\n", "\n")
    return render_template('edit_text.html', content=content, form=form)


@main.route("/edit/open_times", methods=['GET', 'POST'])
@login_required
def edit_opentimes():
    form = OpenTimesForm()
    if form.validate_on_submit():
        cell_00 = form.cell_00.data.replace('\r', '').replace('\n', '<br>')
        cell_01 = form.cell_01.data.replace('\r', '').replace('\n', '<br>')
        cell_10 = form.cell_10.data.replace('\r', '').replace('\n', '<br>')
        cell_11 = form.cell_11.data.replace('\r', '').replace('\n', '<br>')
        cell_20 = form.cell_20.data.replace('\r', '').replace('\n', '<br>')
        cell_21 = form.cell_21.data.replace('\r', '').replace('\n', '<br>')
        cell_30 = form.cell_30.data.replace('\r', '').replace('\n', '<br>')
        cell_31 = form.cell_31.data.replace('\r', '').replace('\n', '<br>')
        cell_40 = form.cell_40.data.replace('\r', '').replace('\n', '<br>')
        cell_41 = form.cell_41.data.replace('\r', '').replace('\n', '<br>')
        cell_50 = form.cell_50.data.replace('\r', '').replace('\n', '<br>')
        cell_51 = form.cell_51.data.replace('\r', '').replace('\n', '<br>')
        cell_60 = form.cell_60.data.replace('\r', '').replace('\n', '<br>')
        cell_61 = form.cell_61.data.replace('\r', '').replace('\n', '<br>')
        content = f"""
|               	| For 'Guests'                      | General Public 	|
|---------------	|-------------------------------	|----------------	|
| **Monday**    	| {cell_00}                         | {cell_01}       	|
| **Tuesday**   	| {cell_10}                     	| {cell_11}       	|
| **Wednesday** 	| {cell_20}                      	| {cell_21}       	|
| **Thursday**  	| {cell_30}                        	| {cell_31}        	|
| **Friday**    	| {cell_40}                      	| {cell_41}       	|
| **Saturday**  	| {cell_50}                     	| {cell_51}       	|
| **Sunday**    	| {cell_60}                      	| {cell_61}         |
"""

        with open("flasksite/templates/markdown/opentimes.md", "w", encoding="utf8") as f:
            f.write(content)
        flash('Content updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        with open("flasksite/templates/markdown/opentimes.md", "r", encoding="utf8") as f:
            content = f.read()
            tbl = content.split('|')
            form.cell_00.data = tbl[10].strip().replace('<br>', '\n')
            form.cell_01.data = tbl[11].strip().replace('<br>', '\n')
            form.cell_10.data = tbl[14].strip().replace('<br>', '\n')
            form.cell_11.data = tbl[15].strip().replace('<br>', '\n')
            form.cell_20.data = tbl[18].strip().replace('<br>', '\n')
            form.cell_21.data = tbl[19].strip().replace('<br>', '\n')
            form.cell_30.data = tbl[22].strip().replace('<br>', '\n')
            form.cell_31.data = tbl[23].strip().replace('<br>', '\n')
            form.cell_40.data = tbl[26].strip().replace('<br>', '\n')
            form.cell_41.data = tbl[27].strip().replace('<br>', '\n')
            form.cell_50.data = tbl[30].strip().replace('<br>', '\n')
            form.cell_51.data = tbl[31].strip().replace('<br>', '\n')
            form.cell_60.data = tbl[34].strip().replace('<br>', '\n')
            form.cell_61.data = tbl[35].strip().replace('<br>', '\n')

    return render_template('edit_openingtimes.html', form=form)