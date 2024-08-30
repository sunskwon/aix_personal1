import styles from "./Components.module.css";

function ChatList({ chatList }) {

    return (
        <>
            <div className={styles.container}>
                {chatList.length > 0 &&
                    <div className={styles.chatBox}>
                        {chatList.map((chat, index) => (
                            <div
                                key={index}
                                className={styles.chat}
                            >
                                <div className={styles.questionBox}>
                                    <p>{chat.question}</p>
                                </div>
                                <div className={styles.answerBox}>
                                    <p>{chat.answer}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                }
            </div>
        </>
    );
};

export default ChatList;