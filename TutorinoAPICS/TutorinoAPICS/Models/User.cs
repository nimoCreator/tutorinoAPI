namespace TutorinoAPICS.Models
{
    public class User
    {
        public int Id { get; set; }
        public String UserName { get; set; }
        public String UserSurname { get; set; }
        public String UserEmail { get; set; }
        public String UserLogin { get; set; }
        public String UserPassword { get; set; }
        public String UserBirthdate { get; set; }
        public String UserPfp { get; set; }
        public String UserStatus { get; set; }
        public Double UserGrade { get; set; }
        public int UserCount { get; set; }
        public bool UserTutor { get; set; }
        public bool UserStudent { set; get; }
        public bool UserOperator { set; get; }
    }
}
