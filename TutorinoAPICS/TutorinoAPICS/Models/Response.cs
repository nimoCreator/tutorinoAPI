namespace TutorinoAPICS.Models
{
    public class Response
    {
        public Response()
        {
            StatusCode = 100;
            ErrorMessage = "No Data Found";
        }
        public int StatusCode { get; set; }
        public string ErrorMessage { get; set; }
    }
}
