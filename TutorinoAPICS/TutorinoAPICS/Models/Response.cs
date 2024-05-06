namespace TutorinoAPICS.Models
{
    public class Response
    {
        public Response()
        {
            StatusCode = 100;
            ErrorMessage = "No Data Found";
        }
        public Response(int statusCode, string errorMessage)
        {
            StatusCode = statusCode;
            ErrorMessage = errorMessage;
        }

        public int StatusCode { get; set; }
        public string ErrorMessage { get; set; }
    }
}
