using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Data;
using System.Data.SqlClient;
using TutorinoAPICS.Models;

namespace TutorinoAPICS.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class UsersController : ControllerBase
    {
        public readonly IConfiguration configuration;
        public UsersController(IConfiguration configuration)
        {
            this.configuration = configuration;
        }

        [HttpGet]
        [Route("getAllUsers")]
        public String GetUsers()
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from users", con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            List<User> users = new List<User>();
            Response response = new Response();
            if (dataTable.Rows.Count > 0)
            {
                for (int i = 0; i < dataTable.Rows.Count; i++)
                {
                    User usr = new User();
                    usr.Id = Convert.ToInt32(dataTable.Rows[i]["uuid"]);
                    usr.UserName = Convert.ToString(dataTable.Rows[i]["name"]);
                    usr.UserSurname = Convert.ToString(dataTable.Rows[i]["surname"]);
                    users.Add(usr);
                }
            }
            if(users.Count>0)
            {
                return JsonConvert.SerializeObject(users);
            }
            else
            {
                return JsonConvert.SerializeObject(response);
            }
        }

        [HttpPost]
        [Route("addUser")]
        public String AddUser(UserAdded newUser)
        {
            int isTutor = 0;
            int isStudent = 0;
            int isOperator = 0;
            switch(newUser.AccountType){
                case "Tutor":
                    isTutor = 1;
                    break;
                case "Student":
                    isStudent = 1;
                    break;
                case "Operator":
                    isOperator = 1;
                    break;
                default:
                    isStudent = 1;
                    break;
            }
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Insert into users(name,surname,login,email,password,is_student,is_tutor,is_operator) values('" + newUser.UserName + "','" + newUser.UserSurname + "','" + newUser.UserLogin + "','" + newUser.UserEmail + "','" + newUser.UserPassword + "','" + isStudent + "','" + isTutor + "','" + isOperator + "')", con);
            con.Open();
            int i;
            try
            {
                i = cmd.ExecuteNonQuery();
            } catch (Exception ex)
            {
                return JsonConvert.SerializeObject(new Response(102, "User Exists"));
            }
            con.Close();
            if (i > 0)
            {
                return JsonConvert.SerializeObject(new Response(0, "Data added"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }

        [HttpPost]
        [Route("loginUser")]
        public String LogUser(UserLogin userData)
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from users where login = '" + userData.Username + "' or email = '" + userData.Email + "'", con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            if (dataTable.Rows.Count > 0)
            {
                if (Convert.ToString(dataTable.Rows[0]["password"]) == userData.Password)
                {
                    return JsonConvert.SerializeObject(new ResponseUser(0, "Access", Convert.ToInt32(dataTable.Rows[0]["uuid"])));
                }
                else
                {
                    return JsonConvert.SerializeObject(new ResponseUser(101, "Wrong Password", 0));
                }
            }
            else
            {
                return JsonConvert.SerializeObject(new ResponseUser(100, "No User", 0));
            }
        }  

        [HttpPost]
        [Route("changeFunction")]
        public String ChangeFunc(UserFunction user)
        {
            int isTutor = 0;
            int isStudent = 0;
            int isOperator = 0;
            switch(user.AccountType){
                case "Tutor":
                    isTutor = 1;
                    break;
                case "Student":
                    isStudent = 1;
                    break;
                case "Operator":
                    isOperator = 1;
                    break;
                default:
                    isStudent = 1;
                    break;
            }
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Update users Set is_student=" + isStudent + ",is_tutor=" + isTutor +",is_operator=" + isOperator + " Where uuid=" + user.userID, con);
            con.Open();
            int i;
            try
            {
                i = cmd.ExecuteNonQuery();
            } catch (Exception ex)
            {
                return JsonConvert.SerializeObject(new Response(102, "Wrong Data"));
            }
            con.Close();
            if (i > 0)
            {
                return JsonConvert.SerializeObject(new Response(0, "Data added"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }   

        [HttpPost]
        [Route("editProfile")]
        public String editProfile(UserEdit user){
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("AppCon").ToString());
            SqlCommand cmd = new SqlCommand("Update users Set birthdate=@birthdate,pfp=@pfp Where uuid=@uuid", con);
            cmd.Parameters.Add("@birthdate", SqlDbType.DateTime).Value = user.birthdate;
            cmd.Parameters.Add("@pfp", SqlDbType.VarChar).Value = user.pfp;
            cmd.Parameters.Add("@uuid", SqlDbType.Int).Value = user.userID;
            con.Open();
            int i;
            try
            {
                i = cmd.ExecuteNonQuery();
            } catch (Exception ex)
            {
                return JsonConvert.SerializeObject(new Response(102, "Internal Error"));
            }
            con.Close();
            if (i > 0)
            {
                return JsonConvert.SerializeObject(new Response(0, "Data Edited"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }
    }
}
