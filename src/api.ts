import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/predict';

export const predict = async (inputData: string[]) => {
  try {
    const response = await axios.post(API_URL, { input: inputData });
    return response.data;
  } catch (error) {
    console.error('Error making prediction:', error);
    throw error;
  }
};
