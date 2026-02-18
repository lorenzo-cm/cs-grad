// src/components/PageTransitionWrapper.tsx
import { motion } from 'framer-motion';
import React from 'react';

const pageTransition = {
  in: {
    opacity: 1,
    x: 0
  },
  out: {
    opacity: 0,
    x: "-100%"
  }
};

const PageTransitionWrapper: React.FC<{children: React.ReactNode}> = ({ children }) => {
  return (
    <motion.div
      initial="out"
      animate="in"
      exit="out"
      variants={pageTransition}
      transition={{ duration: 0.5 }}
    >
      {children}
    </motion.div>
  );
};

export default PageTransitionWrapper;
