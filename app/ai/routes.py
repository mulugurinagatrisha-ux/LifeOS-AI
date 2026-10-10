from flask import render_template, request, jsonify, redirect, url_for,flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Chat, ChatSession, ask_ai

from . import ai
from .forms import ChatForm
from .gemini import ask_ai


@ai.route("/")
@login_required
def chat():

    form = ChatForm()

    session_id = request.args.get("session_id", type=int)

    sessions = ChatSession.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ChatSession.created_at.desc()
    ).all()

    if not sessions:

        first_session = ChatSession(
            title="New Chat",
            user_id=current_user.id
        )

        db.session.add(first_session)
        db.session.commit()

        return redirect(
            url_for(
                "ai.chat",
                session_id=first_session.id
            )
        )

    if session_id is None:
        session_id = sessions[0].id

    chats = Chat.query.filter_by(
        session_id=session_id,
        user_id=current_user.id
    ).order_by(
        Chat.id.asc()
    ).all()

    return render_template(
        "ai/chat.html",
        form=form,
        chats=chats,
        sessions=sessions,
        current_session=session_id
    )


@ai.route("/send", methods=["POST"])
@login_required
def send_message():

    data = request.get_json()

    message = data.get("message", "").strip()

    session_id = data.get("session_id")

    if not message:

        return jsonify({
            "answer": "Please enter a message."
        })

    history = Chat.query.filter_by(
    session_id=session_id,
    user_id=current_user.id
    ).order_by(Chat.id.asc()).all()
    
    conversation = ""
    
    for item in history:
        conversation += f"User: {item.question}\n"
        conversation += f"AI: {item.answer}\n"
    
    prompt = f"""
    You are LifeOS AI.
    
    Continue the conversation naturally.
    
    Previous Conversation:
    {conversation}
    
    Current User Message:
    {message}
    
    Give a helpful, accurate and friendly response.
    """
    
    answer = ask_ai(prompt)

    session = ChatSession.query.get(session_id)
    
    if session:
    
        total_messages = Chat.query.filter_by(
            session_id=session_id
        ).count()
    
        if total_messages == 0:
    
            title = message[:40]
    
            if len(message) > 40:
                title += "..."
    
            session.title = title
    
    chat = Chat(
        question=message,
        answer=answer,
        user_id=current_user.id,
        session_id=session_id
    )
    
    db.session.add(chat)
    db.session.commit()
    

    return jsonify({
        "answer": answer
    })


@ai.route("/new")
@login_required
def new_chat():

    session = ChatSession(
        title="New Chat",
        user_id=current_user.id
    )

    db.session.add(session)
    db.session.commit()

    return redirect(
        url_for(
            "ai.chat",
            session_id=session.id
        )
    )
@ai.route("/rename/<int:id>", methods=["POST"])
@login_required
def rename_chat(id):

    session = ChatSession.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    title = request.form.get("title", "").strip()

    if title:

        session.title = title

        db.session.commit()

        flash("Chat renamed successfully.")

    return redirect(
        url_for(
            "ai.chat",
            session_id=session.id
        )
    )


@ai.route("/delete/<int:id>")
@login_required
def delete_chat(id):

    session = ChatSession.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first_or_404()

    Chat.query.filter_by(
        session_id=session.id
    ).delete()

    db.session.delete(session)

    db.session.commit()

    flash("Chat deleted successfully.")

    latest = ChatSession.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ChatSession.created_at.desc()
    ).first()

    if latest:

        return redirect(
            url_for(
                "ai.chat",
                session_id=latest.id
            )
        )

    return redirect(
        url_for("ai.chat")
    )   
     