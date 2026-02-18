const handleConfirmationSubmit = () => {
      
}

const ConfirmationForm = () => (
    <form onSubmit={handleConfirmationSubmit} className="w-full max-w-xs">
      <div className="mb-4">
        <label htmlFor="confirmationCode" className="block text-gray-700 text-sm font-bold mb-2">Confirmation Code</label>
        <input
          type="text"
          id="confirmationCode"
          name="confirmationCode"
          // Adicione um estado para controlar o valor do input, semelhante ao formData
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div className="flex items-center justify-between">
        <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Confirm
        </button>
      </div>
    </form>
  );

  export default ConfirmationForm;