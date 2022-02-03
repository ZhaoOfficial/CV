#include <iostream>
#include <cstring>
#include <sstream>
#include <cmath>
#include <vector>
#include <initializer_list>

#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

using namespace cv;
using std::string;
using std::ostream;
using std::stringstream;
using std::vector;
using std::initializer_list;
using std::cin;
using std::cout;
using std::endl;
const string storePath = "D:/Mywork/OpenCV/sampleFile/";
const string samplePath = "D:/Mywork/OpenCV/SampleImage/";

static void help(char** argv)
{
    cout
        << argv[0] << " shows the usage of the OpenCV serialization functionality.\n"
        << "usage:\n"
        << argv[0] << " outputfile.yml.gz\n"
        << "The output file may be either XML (xml) or YAML (yml/yaml).\n"
        << "You can even compress it by specifying this in its extension like xml.gz yaml.gz etc...\n"
        << "With FileStorage you can serialize objects in OpenCV by using the << and >> operators.\n"
        << "For example: - create a class and have it serialized\n"
        << "             - use it to read and write matrices." << endl;
}

class MyData
{
public:
    MyData() : A(0), X(0), id("") {}
    // explicit to avoid implicit conversion 
    explicit MyData(int) : A(97), X(CV_PI), id("mydata1234") {}
    //Write serialization for this class
    void write(FileStorage& fs) const
    {
        fs << "{" << "A" << A << "X" << X << "id" << id << "}";
    }
    //Read serialization for this class
    void read(const FileNode& node)
    {
        A = (int)node["A"];
        X = (double)node["X"];
        id = (string)node["id"];
    }

public:
    int A;
    double X;
    string id;
};

//These write and read functions must be defined for the serialization in FileStorage to work
static void write(FileStorage& fs, const std::string&, const MyData& x)
{
    x.write(fs);
}

static void read(const FileNode& node, MyData& x, const MyData& default_value = MyData()) {
    if (node.empty())
        x = default_value;
    else
        x.read(node);
}

// This function will print our custom class to the console
static ostream& operator<<(ostream& out, const MyData& m)
{
    out << "{ id = " << m.id << ", ";
    out << "X = " << m.X << ", ";
    out << "A = " << m.A << "}";
    return out;
}

int main(int argc, char** argv)
{
    if (argc != 2)
    {
        help(argv);
        return 1;
    }

    string filename = storePath + argv[1];
    {
        //write
        Mat R = Mat_<uchar>::eye(3, 3);
        Mat T = Mat_<double>::zeros(3, 1);

        MyData myData(1);
        FileStorage fs(filename, FileStorage::WRITE);
        // or:
        // FileStorage fs;
        // fs.open(filename, FileStorage::WRITE);
        fs << "iterationNr" << 100;
        // text - string sequence
        fs << "strings" << "[";
        fs << "sample image" << "Awesomeness" << samplePath + "baboon.jpg";
        // close sequence
        fs << "]";
        // text - mapping
        fs << "Mapping";
        fs << "{" << "One" << 1;
        fs << "Two" << 2 << "}";
        // cv::Mat
        fs << "R" << R;
        fs << "T" << T;
        // your own data structures
        fs << "MyData" << myData;
        // explicit close
        fs.release();
        cout << "Write Done." << endl;
    }
    {
        //read
        cout << endl << "Reading: " << endl;
        FileStorage fs;
        fs.open(filename, FileStorage::READ);
        int itNr;
        //fs["iterationNr"] >> itNr;
        itNr = (int)fs["iterationNr"];
        cout << "iterationNr: " << itNr << endl;
        if (!fs.isOpened())
        {
            cout << "Failed to open " << filename << endl;
            return 1;
        }
        // Read string sequence - Get node
        FileNode n = fs["strings"];
        if (n.type() != FileNode::SEQ)
        {
            cout << "strings is not a sequence! FAIL" << endl;
            return 1;
        }
        // Go through the node
        FileNodeIterator it = n.begin(), it_end = n.end();
        for (; it != it_end; ++it)
        {
            cout << (string)*it << " ";
        }
        cout << endl;
        // Read mappings from a sequence
        n = fs["Mapping"];
        cout << "Two: " << (int)(n["Two"]) << "; ";
        cout << "One: " << (int)(n["One"]) << endl << endl;

        // Read cv::Mat
        Mat R, T;
        fs["R"] >> R;
        fs["T"] >> T;
        cout << "R =\n" << R << endl;
        cout << "T =\n" << T << endl << endl;
        // Read your own structure_
        MyData m;
        fs["MyData"] >> m;
        cout << "MyData = " << endl << m << endl << endl;
        //Show default behavior for non existing nodes
        cout << "Attempt to read NonExisting (should initialize the data structure with its default).";
        fs["NonExisting"] >> m;
        cout << endl << "NonExisting = " << endl << m << endl;
    }
    cout << endl
        << "Tip: Open up " << filename << " with a text editor to see the serialized data." << endl;
    return 0;
}