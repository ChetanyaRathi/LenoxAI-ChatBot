import React, { useState, useEffect, useRef } from 'react';
import { BsSendFill } from 'react-icons/bs'; // Send icon
import BotIcon from './assets/bot-icon.svg';
import PortfolioLogo from './assets/portfolio-logo.svg';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messageListRef = useRef(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  // Initial bot greeting
  useEffect(() => {
    setMessages([
      {
        sender: 'bot',
        text: "Welcome to Nova! I'm an AI assistant built to answer your questions about Chetanya Rathi's resume. How can I help?"
      }
    ]);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { sender: 'user', text: inputValue };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/query', { // Local backend
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: inputValue }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      const botMessage = { sender: 'bot', text: data.response || "No answer found." };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Fetch error:", error);
      const errorMessage = {
        sender: 'bot',
        text: "Sorry, I'm having trouble connecting. Please check if the local server is running and try again."
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setInputValue('');
    }
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-interface">
        <div className="chat-header">
          <a href="https://chetanyarathi-portfolio.netlify.app/" target="_blank" rel="noopener noreferrer" className="portfolio-logo-link">
            <img src={PortfolioLogo} alt="Portfolio Logo" className="portfolio-logo" />
          </a>
          <div className="header-text">
            <h2>Lenox AI</h2>
            <p>Your AI guide to Chetanya's profile</p>
          </div>
        </div>

        <div className="message-list" ref={messageListRef}>
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-container ${msg.sender}`}>
              {msg.sender === 'bot' && <img src={BotIcon} alt="Bot Icon" className="bot-icon" />}
              <div className={`message ${msg.sender}`}>{msg.text}</div>
            </div>
          ))}

          {isLoading && (
            <div className="message-container bot">
              <img src={BotIcon} alt="Bot Icon" className="bot-icon" />
              <div className="message bot loading-animation">
                <span></span><span></span><span></span>
              </div>
            </div>
          )}
        </div>

        <form className="message-form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask about projects, skills, experience..."
            disabled={isLoading}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) handleSubmit(e);
            }}
          />
          <button type="submit" disabled={isLoading || !inputValue.trim()}>
            <BsSendFill />
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
