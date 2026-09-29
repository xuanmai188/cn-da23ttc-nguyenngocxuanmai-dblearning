import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { quizApi } from '../api/quizApi';
import { learningApi } from '../api/learningApi';
import { motion, AnimatePresence } from 'framer-motion';
import { XMarkIcon, ChevronLeftIcon, ChevronRightIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

export default function Flashcard() {
  const { itemId } = useParams();
  const navigate = useNavigate();
  const [flashcards, setFlashcards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const cards = await quizApi.getFlashcards(itemId);
        setFlashcards(cards);
        const sess = await learningApi.startSession(itemId);
        setSession(sess);
      } catch (err) {
        console.error("Error", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [itemId]);

  const handleFinish = async () => {
    if (session) {
      await learningApi.endSession(session.id);
    }
    navigate('/topics');
  };

  const nextCard = () => {
    if (currentIndex < flashcards.length - 1) {
      setIsFlipped(false);
      setTimeout(() => setCurrentIndex(c => c + 1), 150);
    }
  };

  const prevCard = () => {
    if (currentIndex > 0) {
      setIsFlipped(false);
      setTimeout(() => setCurrentIndex(c => c - 1), 150);
    }
  };

  if (loading) return <div className="h-screen flex items-center justify-center bg-gray-900 text-white">Đang tải flashcards...</div>;
  if (!flashcards.length) return <div className="h-screen flex items-center justify-center bg-gray-900 text-white">Không có thẻ nào</div>;

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-4">
      <button onClick={handleFinish} className="absolute top-6 right-6 text-gray-400 hover:text-white transition-colors">
        <XMarkIcon className="h-8 w-8" />
      </button>

      <div className="w-full max-w-2xl">
        <div className="text-gray-400 text-sm font-medium mb-4 flex justify-between items-center">
          <span>Học Flashcards</span>
          <span>{currentIndex + 1} / {flashcards.length}</span>
        </div>
        
        {/* Progress bar */}
        <div className="w-full bg-gray-700 h-1.5 rounded-full mb-12">
          <div 
            className="bg-primary-500 h-1.5 rounded-full transition-all duration-300" 
            style={{ width: `${((currentIndex + 1) / flashcards.length) * 100}%` }}
          ></div>
        </div>

        {/* Card */}
        <div className="relative w-full aspect-[4/3] perspective-1000">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentIndex + (isFlipped ? '-back' : '-front')}
              initial={{ rotateX: isFlipped ? -90 : 90, opacity: 0 }}
              animate={{ rotateX: 0, opacity: 1 }}
              exit={{ rotateX: isFlipped ? 90 : -90, opacity: 0 }}
              transition={{ duration: 0.3 }}
              onClick={() => setIsFlipped(!isFlipped)}
              className="absolute inset-0 w-full h-full bg-white rounded-2xl shadow-2xl cursor-pointer flex flex-col items-center justify-center p-10 text-center select-none"
              style={{ transformStyle: 'preserve-3d' }}
            >
              <ArrowPathIcon className="absolute top-4 right-4 h-6 w-6 text-gray-300" />
              <h2 className="text-2xl md:text-4xl font-bold text-gray-800 leading-tight">
                {isFlipped ? flashcards[currentIndex].answer : flashcards[currentIndex].question}
              </h2>
              <p className="absolute bottom-6 text-gray-400 text-sm font-medium">Nhấp để lật</p>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Controls */}
        <div className="flex items-center justify-center space-x-8 mt-12">
          <button 
            onClick={prevCard}
            disabled={currentIndex === 0}
            className="p-4 rounded-full bg-gray-800 text-white disabled:opacity-30 hover:bg-gray-700 transition-colors"
          >
            <ChevronLeftIcon className="h-6 w-6" />
          </button>
          
          <button 
            onClick={() => setIsFlipped(!isFlipped)}
            className="px-8 py-3 rounded-full bg-primary-600 text-white font-semibold hover:bg-primary-700 transition-colors"
          >
            Lật thẻ
          </button>

          <button 
            onClick={currentIndex === flashcards.length - 1 ? handleFinish : nextCard}
            className={`p-4 rounded-full text-white transition-colors ${
              currentIndex === flashcards.length - 1 ? 'bg-green-600 hover:bg-green-700' : 'bg-gray-800 hover:bg-gray-700'
            }`}
          >
            {currentIndex === flashcards.length - 1 ? (
              <span className="font-bold px-4">Xong</span>
            ) : (
              <ChevronRightIcon className="h-6 w-6" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
