import os

file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Quiz.jsx"
content = """import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { quizApi } from '../api/quizApi';
import { learningApi } from '../api/learningApi';
import { motion } from 'framer-motion';
import { XMarkIcon, ClockIcon, ClipboardDocumentListIcon } from '@heroicons/react/24/outline';
import clsx from 'clsx';

export default function Quiz() {
  const { itemId } = useParams();
  const navigate = useNavigate();
  const [quizInfo, setQuizInfo] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState(null);
  
  // History state
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await quizApi.getQuiz(itemId);
        setQuizInfo(data);
        setQuestions(data.questions || []);
        
        try {
          const hist = await quizApi.getQuizHistory(itemId);
          setHistory(hist || []);
          if (hist && hist.length === 0) {
            setShowHistory(false); // If no history, skip history screen
            const sess = await learningApi.startSession(itemId);
            setSession(sess);
          }
        } catch (e) {
          console.error("No history or failed to fetch", e);
          setShowHistory(false);
          const sess = await learningApi.startSession(itemId);
          setSession(sess);
        }
      } catch (err) {
        console.error("Error", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [itemId]);

  const handleStartQuiz = async () => {
    setShowHistory(false);
    setAnswers({});
    setResult(null);
    try {
      const sess = await learningApi.startSession(itemId);
      setSession(sess);
    } catch (e) {}
  };

  const handleSelect = (qId, optionIdx) => {
    if (result) return;
    setAnswers({ ...answers, [qId]: optionIdx });
  };

  const handleSubmit = async () => {
    try {
      const res = await quizApi.submitQuiz(itemId, answers);
      setResult(res);
      if (session) {
        await learningApi.endSession(session.id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="h-screen bg-gray-50 flex justify-center items-center">Đang tải câu hỏi...</div>;
  if (!questions.length) return <div className="p-8">Không có câu hỏi nào</div>;

  const totalPages = Math.ceil(history.length / itemsPerPage);
  const currentHistory = history.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  if (showHistory) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg max-w-2xl w-full p-8 relative">
          <button onClick={() => navigate('/topics')} className="absolute top-4 right-4 p-2 rounded-full hover:bg-gray-100">
            <XMarkIcon className="h-6 w-6 text-gray-500" />
          </button>
          
          <div className="flex items-center mb-6">
            <div className="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center mr-4">
              <ClipboardDocumentListIcon className="h-6 w-6 text-primary-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{quizInfo?.title}</h2>
              <p className="text-gray-500">Lịch sử làm bài kiểm tra</p>
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b-2 border-gray-100">
                  <th className="py-3 px-4 font-semibold text-gray-600">Lần thi</th>
                  <th className="py-3 px-4 font-semibold text-gray-600">Điểm</th>
                  <th className="py-3 px-4 font-semibold text-gray-600">Kết quả</th>
                  <th className="py-3 px-4 font-semibold text-gray-600">Ngày làm</th>
                </tr>
              </thead>
              <tbody>
                {currentHistory.map((h, i) => (
                  <tr key={h.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                    <td className="py-4 px-4 font-medium text-gray-900">Lần {history.length - ((currentPage - 1) * itemsPerPage + i)}</td>
                    <td className="py-4 px-4 font-bold text-primary-600">{h.score}</td>
                    <td className="py-4 px-4">
                      <span className={clsx("px-3 py-1 rounded-full text-xs font-bold", h.is_passed ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700")}>
                        {h.is_passed ? "ĐẠT" : "CHƯA ĐẠT"}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-500">
                      {new Date(h.taken_at).toLocaleDateString('vi-VN')} {new Date(h.taken_at).toLocaleTimeString('vi-VN')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <div className="flex justify-center mt-6 space-x-2">
              <button 
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="px-3 py-1 rounded border hover:bg-gray-50 disabled:opacity-50"
              >
                Trước
              </button>
              <span className="px-4 py-1 text-gray-600">Trang {currentPage} / {totalPages}</span>
              <button 
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="px-3 py-1 rounded border hover:bg-gray-50 disabled:opacity-50"
              >
                Sau
              </button>
            </div>
          )}
          
          <div className="mt-8 text-center">
            <button
              onClick={handleStartQuiz}
              className="bg-primary-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-primary-700 transition-colors"
            >
              Làm lại bài kiểm tra
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm h-16 flex items-center justify-between px-6 sticky top-0 z-10">
        <div className="flex items-center text-gray-800 font-bold">
          <ClockIcon className="h-5 w-5 mr-2 text-primary-500" />
          Bài kiểm tra
        </div>
        <button onClick={() => navigate('/topics')} className="p-2 rounded-full hover:bg-gray-100">
          <XMarkIcon className="h-6 w-6 text-gray-500" />
        </button>
      </header>

      <main className="flex-1 max-w-3xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8 pb-32">
        {result && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow p-8 text-center border-t-4 border-green-500"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Kết quả bài làm</h2>
            <div className="text-5xl font-black text-primary-600 mb-4">
              {result.score} <span className="text-2xl text-gray-400">/ 100</span>
            </div>
            <p className="text-gray-600 text-lg">
              Đúng {result.details.filter(d => d.is_correct).length} / {questions.length} câu hỏi
            </p>
          </motion.div>
        )}

        {questions.map((q, idx) => {
          let qResult = null;
          if (result) {
            qResult = result.details.find(d => d.question_id === q.id);
          }

          return (
            <div key={q.id} className="bg-white rounded-2xl shadow-sm p-6 sm:p-8 border border-gray-100">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">
                <span className="text-primary-600 mr-2">Câu {idx + 1}.</span> 
                {q.content}
              </h3>
              
              <div className="space-y-3">
                {q.options.map((opt, optIdx) => {
                  const isSelected = answers[q.id] === optIdx;
                  let optClass = "border-gray-200 hover:border-primary-500 hover:bg-primary-50";
                  
                  if (isSelected) optClass = "border-primary-500 bg-primary-50 text-primary-900";
                  
                  if (result) {
                    if (qResult?.correct_option === optIdx) {
                      optClass = "border-green-500 bg-green-50 text-green-900 ring-2 ring-green-500";
                    } else if (isSelected && !qResult?.is_correct) {
                      optClass = "border-red-500 bg-red-50 text-red-900";
                    } else {
                      optClass = "border-gray-200 opacity-50";
                    }
                  }

                  return (
                    <button
                      key={optIdx}
                      disabled={!!result}
                      onClick={() => handleSelect(q.id, optIdx)}
                      className={clsx(
                        "w-full text-left p-4 rounded-xl border-2 transition-all font-medium",
                        optClass
                      )}
                    >
                      <span className="inline-block w-8 font-bold text-gray-400 mr-2">
                        {String.fromCharCode(65 + optIdx)}.
                      </span>
                      {opt}
                    </button>
                  );
                })}
              </div>
              
              {result && qResult && (
                <div className={`mt-6 p-4 rounded-lg ${qResult.is_correct ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                  <p className="font-bold mb-1">{qResult.is_correct ? 'Chính xác!' : 'Sai rồi!'}</p>
                  <p className="text-sm">{qResult.explanation}</p>
                </div>
              )}
            </div>
          );
        })}

        {!result && (
          <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-10">
            <div className="max-w-3xl mx-auto flex justify-between items-center">
              <span className="text-gray-500 font-medium">
                Đã chọn {Object.keys(answers).length} / {questions.length} câu
              </span>
              <button
                onClick={handleSubmit}
                disabled={Object.keys(answers).length < questions.length}
                className="bg-primary-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Nộp bài
              </button>
            </div>
          </div>
        )}
        
        {result && (
          <div className="text-center mt-8 space-x-4">
            <button
              onClick={() => {
                setShowHistory(true);
                // Also optionally refresh history from API here
                quizApi.getQuizHistory(itemId).then(h => {
                   setHistory(h || []);
                   setCurrentPage(1);
                }).catch(e => console.error(e));
              }}
              className="bg-gray-200 text-gray-800 px-8 py-3 rounded-xl font-bold hover:bg-gray-300 transition-colors"
            >
              Xem Lịch sử
            </button>
            <button
              onClick={() => navigate('/topics')}
              className="bg-gray-900 text-white px-8 py-3 rounded-xl font-bold hover:bg-gray-800 transition-colors"
            >
              Trở về danh sách
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Quiz.jsx updated")
