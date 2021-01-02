package ca.cmpt383.project.model;

public class ClassificationResult {
    int rank;
    String result;

    public ClassificationResult(int rank, String result) {
        this.rank = rank;
        this.result = result;
    }

    public int getRank() {
        return rank;
    }

    public void setRank(int rank) {
        this.rank = rank;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "Rank{" +
                "rank=" + rank +
                ", result='" + result + '\'' +
                '}';
    }
}
