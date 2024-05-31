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

    public class ResponseUser{
        public int StatusCode {get;set;}
        public string ErrorCode {get;set;}
        public int UserID {get;set;}

        public ResponseUser(){
            StatusCode = 100;
            ErrorCode = "No Data Found";
            UserID = 0;
        }

        public ResponseUser(int statusCode, string errorMessage, int userID)
        {
            StatusCode = statusCode;
            ErrorCode = errorMessage;
            UserID = userID;
        }
    }
}
