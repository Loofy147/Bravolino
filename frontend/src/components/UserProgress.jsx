import React from 'react';

const UserProgress = ({ subject, progress }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h4 className="text-lg font-bold">{subject}</h4>
      <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
        <div
          className="bg-blue-600 h-2.5 rounded-full"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <p className="text-sm text-gray-500 mt-2">{progress}% complete</p>
    </div>
  );
};

export default UserProgress;
